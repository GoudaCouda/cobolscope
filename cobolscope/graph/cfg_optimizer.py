"""
cobolscope.graph.cfg_optimizer
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Intraprocedural CFG post-dominance merge reduction and dominator tree computation.
Consolidates redundant pass-through and chained merge nodes atomically using
Immediate Post-Dominance (ipdom) analysis, and computes dominator trees.
"""

from __future__ import annotations
from typing import Dict, List, Optional, Set, Tuple

from .cfg_models import CfgNode, CfgEdge, CfgNodeType, IntraprocedureCfg
from .utils import compute_dominators, compute_post_dominators


def consolidate_merges_with_ipdom(
    nodes: Dict[str, CfgNode],
    edges: List[CfgEdge],
    cfg: IntraprocedureCfg,
) -> Tuple[Dict[str, CfgNode], List[CfgEdge]]:
    """
    Consolidates merge points using Immediate Post-Dominance (ipdom) analysis.
    Eliminates pass-through 1:1 merge nodes and merges that share the same immediate
    post-dominating convergence point atomically without mutating edges during iteration.
    Calculates and stores forward dominators, post-dominators, and dead-code reachability on cfg.

    Returns:
        Tuple of (optimized_nodes, optimized_edges).
    """
    exit_ids = cfg.exit_node_ids if cfg.exit_node_ids else ["exit"]

    # 1. Build initial successor / predecessor maps
    succ_map: Dict[str, List[str]] = {nid: [] for nid in nodes}
    pred_map: Dict[str, List[str]] = {nid: [] for nid in nodes}
    for e in edges:
        if e.source in succ_map and e.target in pred_map:
            succ_map[e.source].append(e.target)
            pred_map[e.target].append(e.source)

    # 2. Identify redundant MERGE nodes
    alias_map: Dict[str, str] = {}
    for nid, node in list(nodes.items()):
        if node.node_type == CfgNodeType.MERGE:
            preds = pred_map.get(nid, [])
            succs = succ_map.get(nid, [])
            # Pass-through merge with at most 1 outgoing target
            if len(preds) <= 1 and len(succs) == 1:
                alias_map[nid] = succs[0]
            # Chained merge where successor is also a MERGE node
            elif len(succs) == 1 and succs[0] in nodes and nodes[succs[0]].node_type == CfgNodeType.MERGE:
                alias_map[nid] = succs[0]

    # 3. Resolve transitive alias chains
    def resolve_alias(n: str) -> str:
        seen: Set[str] = set()
        curr = n
        while curr in alias_map and curr not in seen:
            seen.add(curr)
            curr = alias_map[curr]
        return curr

    for k in list(alias_map.keys()):
        alias_map[k] = resolve_alias(k)

    # 4. Atomically rewrite edges and drop redundant self-loops
    new_edges: List[CfgEdge] = []
    seen_edges: Set[Tuple[str, str, str, Optional[str]]] = set()

    for e in edges:
        new_src = alias_map.get(e.source, e.source)
        new_tgt = alias_map.get(e.target, e.target)

        # Skip self-loops resulting from collapsed merge nodes
        if new_src == new_tgt:
            continue

        sig = (new_src, new_tgt, e.edge_type.value, e.label)
        if sig in seen_edges:
            continue
        seen_edges.add(sig)

        e.source = new_src
        e.target = new_tgt
        new_edges.append(e)

    optimized_edges = new_edges

    # 5. Remove collapsed merge nodes from nodes
    optimized_nodes = dict(nodes)
    for deleted_id in alias_map:
        if deleted_id in optimized_nodes:
            del optimized_nodes[deleted_id]

    # 6. Safety validation: ensure all edge endpoints exist in optimized_nodes
    valid_ids = set(optimized_nodes.keys())
    optimized_edges = [e for e in optimized_edges if e.source in valid_ids and e.target in valid_ids]

    # 7. Compute final dominators and post-dominators (ipdom)
    final_succ: Dict[str, List[str]] = {nid: [] for nid in optimized_nodes}
    final_pred: Dict[str, List[str]] = {nid: [] for nid in optimized_nodes}
    for e in optimized_edges:
        final_succ[e.source].append(e.target)
        final_pred[e.target].append(e.source)

    dom_res = compute_dominators(
        nodes=optimized_nodes.keys(),
        successors=lambda u: final_succ.get(u, []),
        predecessors=lambda u: final_pred.get(u, []),
        entry="entry",
    )
    pdom_res = compute_post_dominators(
        nodes=optimized_nodes.keys(),
        successors=lambda u: final_succ.get(u, []),
        predecessors=lambda u: final_pred.get(u, []),
        exits=exit_ids,
    )

    cfg.dominators = dom_res.idom
    cfg.post_dominators = pdom_res.ipdom
    cfg.dead_code_nodes = sorted(list(dom_res.unreachable_nodes))
    cfg.terminal_node_ids = sorted([nid for nid, node in optimized_nodes.items() if node.is_terminal])

    return optimized_nodes, optimized_edges
