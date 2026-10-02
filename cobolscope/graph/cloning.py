"""
cobolscope.graph.cloning
~~~~~~~~~~~~~~~~~~~~~~~~

Intelligent node cloning transformation engine for high in-degree utility routines.
Disentangles complex COBOL procedure call graphs (100 to 200+ nodes) by cloning
leaf utility paragraphs locally per caller section or per caller, eliminating
cross-canvas edge spaghetti.
"""

from __future__ import annotations
from typing import Dict, List, Optional, Set
from collections import defaultdict
import copy

from .models import CallGraph, CallGraphNode, CallGraphEdge, CallGraphCluster, GraphEdgeType


def identify_clone_candidates(
    graph: CallGraph,
    min_in_degree: int = 3,
    max_out_degree: int = 1,
) -> List[str]:
    """
    Identifies candidate procedures eligible for cloning based on mathematical heuristics:
    1. In-degree >= min_in_degree (called from multiple procedures)
    2. Out-degree <= max_out_degree (leaf or near-leaf utility, e.g. logging, formatting, terminal)
    3. Not the entry point
    4. Callers span across >= 2 distinct sections (or distinct caller procedures)

    Args:
        graph: The CallGraph to inspect.
        min_in_degree: Minimum incoming callers to trigger candidate eligibility (default 3).
        max_out_degree: Maximum outgoing calls permitted for a cloneable utility (default 1).

    Returns:
        List of routine names eligible for cloning.
    """
    in_edges: Dict[str, List[CallGraphEdge]] = defaultdict(list)
    out_edges: Dict[str, List[CallGraphEdge]] = defaultdict(list)

    for edge in graph.edges:
        if edge.source in graph.nodes and edge.target in graph.nodes:
            if edge.source != edge.target:
                in_edges[edge.target].append(edge)
                out_edges[edge.source].append(edge)

    candidates = []

    for name, node in graph.nodes.items():
        if node.is_entry_point or node.is_clone:
            continue

        callers = [e.source for e in in_edges[name]]
        if len(callers) < min_in_degree:
            continue

        # Check out-degree
        callees = [e.target for e in out_edges[name]]
        if len(callees) > max_out_degree:
            continue

        # If it has 1 callee, ensure it is an exit paragraph, dummy return, or terminal
        if len(callees) == 1:
            target_node = graph.nodes.get(callees[0])
            if target_node and not (target_node.is_terminal or target_node.is_exit_paragraph or "EXIT" in target_node.name.upper()):
                continue

        # Check section dispersion: callers must belong to >= 2 distinct sections
        caller_sections = set()
        for c in callers:
            c_node = graph.nodes.get(c)
            sec = (c_node.section or "").strip().upper() if c_node else ""
            caller_sections.add(sec if sec else c)

        if len(caller_sections) >= 2 or len(callers) >= 4:
            candidates.append(name)

    # Sort descending by in-degree
    candidates.sort(key=lambda c: len(in_edges[c]), reverse=True)
    return candidates


def apply_node_cloning(
    graph: CallGraph,
    mode: str = "section",
    min_in_degree: int = 3,
    max_out_degree: int = 1,
) -> CallGraph:
    """
    Transforms a CallGraph by cloning eligible utility/leaf routines to disentangle
    cross-graph edge crossings.

    Args:
        graph: Original CallGraph.
        mode: Cloning strategy:
              - 'section': Generates 1 clone per calling section (recommended, preserves visual hierarchy).
              - 'caller': Generates 1 clone per calling procedure (maximum edge reduction).
        min_in_degree: In-degree threshold (default 3).
        max_out_degree: Out-degree threshold (default 1).

    Returns:
        Transformed CallGraph with cloned utility nodes and localized edges.
    """
    candidates = identify_clone_candidates(graph, min_in_degree=min_in_degree, max_out_degree=max_out_degree)
    if not candidates:
        return graph

    # Deep copy the graph so original remains unmodified
    new_graph = graph.model_copy(deep=True)
    total_clones_created = 0

    candidate_set = set(candidates)

    for cand_name in candidates:
        original_node = new_graph.nodes.get(cand_name)
        if not original_node:
            continue

        # Find incoming edges to this candidate
        cand_in_edges = [e for e in new_graph.edges if e.target == cand_name and e.source != cand_name]
        if len(cand_in_edges) < min_in_degree:
            continue

        # Find any outgoing edges from this candidate
        cand_out_edges = [e for e in new_graph.edges if e.source == cand_name and e.target != cand_name]

        if mode == "caller":
            # Group: 1 caller per edge (after the first caller, which stays with the original node)
            total_callers = len(cand_in_edges)
            original_node.clone_total = total_callers
            original_node.clone_index = 1

            for idx, edge in enumerate(cand_in_edges[1:], start=2):
                caller_name = edge.source
                caller_node = new_graph.nodes.get(caller_name)
                clone_id = f"{original_node.id}_c{idx}"
                clone_name = f"{original_node.name}#{idx}"

                # Create clone node
                clone_node = original_node.model_copy(deep=True)
                clone_node.id = clone_id
                clone_node.name = clone_name
                clone_node.is_clone = True
                clone_node.original_name = original_node.name
                clone_node.clone_index = idx
                clone_node.clone_total = total_callers
                clone_node.clone_caller = caller_name
                if caller_node:
                    clone_node.section = caller_node.section
                    clone_node.cluster_id = caller_node.cluster_id

                new_graph.nodes[clone_name] = clone_node
                total_clones_created += 1

                # Retarget incoming edge from caller to clone
                edge.target = clone_name

                # Replicate outgoing edge from clone if applicable
                for out_edge in cand_out_edges:
                    new_graph.edges.append(CallGraphEdge(
                        source=clone_name,
                        target=out_edge.target,
                        edge_type=out_edge.edge_type,
                        label=out_edge.label,
                    ))

                # If caller has a cluster, add clone to caller's cluster
                if caller_node:
                    for cluster in new_graph.clusters:
                        if cluster.id == caller_node.cluster_id and clone_id not in cluster.node_ids:
                            cluster.node_ids.append(clone_id)

        else:
            # mode == "section": Group callers by section
            section_groups: Dict[str, List[CallGraphEdge]] = defaultdict(list)
            for edge in cand_in_edges:
                caller_node = new_graph.nodes.get(edge.source)
                sec = (caller_node.section or "").strip() if caller_node else ""
                group_key = sec if sec else edge.source
                section_groups[group_key].append(edge)

            if len(section_groups) <= 1:
                # All callers are in the same section, no cross-section cloning needed
                continue

            total_groups = len(section_groups)
            group_keys = list(section_groups.keys())

            # First section keeps the original node
            primary_sec = group_keys[0]
            original_node.clone_total = total_groups
            original_node.clone_index = 1

            for idx, sec_key in enumerate(group_keys[1:], start=2):
                edges_in_group = section_groups[sec_key]
                first_caller = new_graph.nodes.get(edges_in_group[0].source)
                clone_id = f"{original_node.id}_sec_{idx}"
                clean_sec_label = sec_key[:12] if len(sec_key) > 12 else sec_key
                clone_name = f"{original_node.name} [{clean_sec_label}]"

                # Create clone node
                clone_node = original_node.model_copy(deep=True)
                clone_node.id = clone_id
                clone_node.name = clone_name
                clone_node.is_clone = True
                clone_node.original_name = original_node.name
                clone_node.clone_index = idx
                clone_node.clone_total = total_groups
                clone_node.clone_caller = sec_key
                if first_caller:
                    clone_node.section = first_caller.section
                    clone_node.cluster_id = first_caller.cluster_id

                new_graph.nodes[clone_name] = clone_node
                total_clones_created += 1

                # Retarget all incoming edges in this section group to the clone
                for edge in edges_in_group:
                    edge.target = clone_name

                # Replicate outgoing edge from clone if applicable
                for out_edge in cand_out_edges:
                    new_graph.edges.append(CallGraphEdge(
                        source=clone_name,
                        target=out_edge.target,
                        edge_type=out_edge.edge_type,
                        label=out_edge.label,
                    ))

                # Add clone to caller's cluster
                if first_caller:
                    for cluster in new_graph.clusters:
                        if cluster.id == first_caller.cluster_id and clone_id not in cluster.node_ids:
                            cluster.node_ids.append(clone_id)

    new_graph.cloned_node_count = total_clones_created

    # Recompute called_by and successors on all nodes
    for node in new_graph.nodes.values():
        node.called_by = []
        node.successors = []

    for edge in new_graph.edges:
        src = new_graph.nodes.get(edge.source)
        tgt = new_graph.nodes.get(edge.target)
        if src and edge.target not in src.successors:
            src.successors.append(edge.target)
        if tgt and edge.source not in tgt.called_by:
            tgt.called_by.append(edge.source)

    return new_graph
