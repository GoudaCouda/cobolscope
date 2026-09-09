"""
cobolscope.graph.utils
~~~~~~~~~~~~~~~~~~~~~~

Compiler-grade, zero-dependency static graph algorithms:
1. Tarjan's Strongly Connected Components (SCC) & Condensation DAG Depth
2. Cooper-Harvey-Kennedy (2001) Dominator Tree (idom) & Dead Code Reachability
3. Immediate Post-Dominator Tree (ipdom) & Dual-Graph Convergence Analysis
"""

from __future__ import annotations
from dataclasses import dataclass, field
from typing import Any, Callable, Dict, Generic, Iterable, List, Optional, Set, Tuple, TypeVar

T = TypeVar("T")


@dataclass
class SccResult(Generic[T]):
    """Results of Tarjan's Strongly Connected Components analysis."""
    sccs: List[List[T]] = field(default_factory=list)
    cycles: List[List[T]] = field(default_factory=list)
    has_cycles: bool = False
    node_to_scc: Dict[T, int] = field(default_factory=dict)
    condensation_adjacency: Dict[int, Set[int]] = field(default_factory=dict)
    max_depth: int = 0


@dataclass
class DominatorResult(Generic[T]):
    """Results of forward dominator tree analysis."""
    idom: Dict[T, Optional[T]] = field(default_factory=dict)
    dom_tree: Dict[T, List[T]] = field(default_factory=dict)
    reachable_nodes: Set[T] = field(default_factory=set)
    unreachable_nodes: Set[T] = field(default_factory=set)


@dataclass
class PostDominatorResult(Generic[T]):
    """Results of immediate post-dominator (ipdom) analysis."""
    ipdom: Dict[T, Optional[T]] = field(default_factory=dict)
    post_dom_tree: Dict[T, List[T]] = field(default_factory=dict)
    reaches_exit: Set[T] = field(default_factory=set)
    dead_ends: Set[T] = field(default_factory=set)


def tarjan_scc(
    nodes: Iterable[T],
    successors: Callable[[T], Iterable[T]],
) -> SccResult[T]:
    """
    Computes Strongly Connected Components (SCCs) via Tarjan's algorithm.
    Runs iteratively to prevent recursion stack overflow on deep graphs.
    Time Complexity: O(|V| + |E|), Space Complexity: O(|V|).
    """
    node_list = list(nodes)
    node_set = set(node_list)
    index = 0
    indices: Dict[T, int] = {}
    lowlink: Dict[T, int] = {}
    stack: List[T] = []
    on_stack: Set[T] = set()
    sccs: List[List[T]] = []

    for root in node_list:
        if root in indices:
            continue

        call_stack: List[Tuple[T, Any]] = [(root, iter(list(successors(root))))]
        indices[root] = lowlink[root] = index
        index += 1
        stack.append(root)
        on_stack.add(root)

        while call_stack:
            u, children_iter = call_stack[-1]
            try:
                v = next(children_iter)
                if v not in node_set:
                    continue
                if v not in indices:
                    indices[v] = lowlink[v] = index
                    index += 1
                    stack.append(v)
                    on_stack.add(v)
                    call_stack.append((v, iter(list(successors(v)))))
                elif v in on_stack:
                    lowlink[u] = min(lowlink[u], indices[v])
            except StopIteration:
                call_stack.pop()
                if call_stack:
                    parent = call_stack[-1][0]
                    lowlink[parent] = min(lowlink[parent], lowlink[u])

                if lowlink[u] == indices[u]:
                    scc: List[T] = []
                    while True:
                        w = stack.pop()
                        on_stack.remove(w)
                        scc.append(w)
                        if w == u:
                            break
                    sccs.append(scc)

    node_to_scc: Dict[T, int] = {}
    for i, scc in enumerate(sccs):
        for n in scc:
            node_to_scc[n] = i

    cycles: List[List[T]] = []
    for scc in sccs:
        if len(scc) > 1:
            cycles.append(scc)
        elif len(scc) == 1:
            n = scc[0]
            if n in set(successors(n)):
                cycles.append(scc)

    has_cycles = len(cycles) > 0

    condensation_adj: Dict[int, Set[int]] = {i: set() for i in range(len(sccs))}
    for u in node_list:
        u_scc = node_to_scc[u]
        for v in successors(u):
            if v in node_to_scc:
                v_scc = node_to_scc[v]
                if u_scc != v_scc:
                    condensation_adj[u_scc].add(v_scc)

    depth_memo: Dict[int, int] = {}
    for scc_idx in range(len(sccs)):
        succs = condensation_adj[scc_idx]
        if not succs:
            depth_memo[scc_idx] = len(sccs[scc_idx])
        else:
            depth_memo[scc_idx] = len(sccs[scc_idx]) + max(depth_memo.get(nxt, 0) for nxt in succs)

    max_depth = max(depth_memo.values(), default=0)

    return SccResult(
        sccs=sccs,
        cycles=cycles,
        has_cycles=has_cycles,
        node_to_scc=node_to_scc,
        condensation_adjacency=condensation_adj,
        max_depth=max_depth,
    )


def compute_dominators(
    nodes: Iterable[T],
    successors: Callable[[T], Iterable[T]],
    predecessors: Callable[[T], Iterable[T]],
    entry: T,
) -> DominatorResult[T]:
    """
    Computes immediate dominators (idom) using the Cooper-Harvey-Kennedy (2001) algorithm.
    Identifies reachable nodes and dead-code unreachable nodes.
    Time Complexity: O(|V| * |E|), Space Complexity: O(|V|).
    """
    node_set = set(nodes)
    if entry not in node_set:
        return DominatorResult(
            idom={},
            dom_tree={},
            reachable_nodes=set(),
            unreachable_nodes=node_set,
        )

    post_order: List[T] = []
    visited: Set[T] = set([entry])
    stack: List[Tuple[T, Any]] = [(entry, iter(list(successors(entry))))]

    while stack:
        u, it = stack[-1]
        try:
            v = next(it)
            if v in node_set and v not in visited:
                visited.add(v)
                stack.append((v, iter(list(successors(v)))))
        except StopIteration:
            stack.pop()
            post_order.append(u)

    rpo = list(reversed(post_order))
    rpo_num: Dict[T, int] = {node: i for i, node in enumerate(rpo)}
    reachable_nodes = set(rpo)
    unreachable_nodes = node_set - reachable_nodes

    doms: Dict[T, T] = {entry: entry}

    def intersect(b1: T, b2: T) -> T:
        finger1, finger2 = b1, b2
        while finger1 != finger2:
            while rpo_num[finger1] > rpo_num[finger2]:
                finger1 = doms[finger1]
            while rpo_num[finger2] > rpo_num[finger1]:
                finger2 = doms[finger2]
        return finger1

    changed = True
    while changed:
        changed = False
        for u in rpo[1:]:
            preds_processed = [p for p in predecessors(u) if p in doms and p in reachable_nodes]
            if not preds_processed:
                continue
            new_idom = preds_processed[0]
            for p in preds_processed[1:]:
                new_idom = intersect(p, new_idom)
            if doms.get(u) != new_idom:
                doms[u] = new_idom
                changed = True

    idom: Dict[T, Optional[T]] = {entry: None}
    dom_tree: Dict[T, List[T]] = {n: [] for n in reachable_nodes}
    for n in rpo[1:]:
        parent = doms.get(n)
        idom[n] = parent
        if parent is not None and parent in dom_tree:
            dom_tree[parent].append(n)

    return DominatorResult(
        idom=idom,
        dom_tree=dom_tree,
        reachable_nodes=reachable_nodes,
        unreachable_nodes=unreachable_nodes,
    )


def compute_post_dominators(
    nodes: Iterable[T],
    successors: Callable[[T], Iterable[T]],
    predecessors: Callable[[T], Iterable[T]],
    exits: Iterable[T],
) -> PostDominatorResult[T]:
    """
    Computes immediate post-dominators (ipdom) by executing dominance on the dual reversed graph.
    If multiple exits exist, introduces a virtual exit node as the root of the reversed graph.
    """
    node_set = set(nodes)
    exit_list = [e for e in exits if e in node_set]

    if not exit_list:
        return PostDominatorResult(
            ipdom={},
            post_dom_tree={},
            reaches_exit=set(),
            dead_ends=node_set,
        )

    if len(exit_list) == 1:
        single_exit = exit_list[0]
        dom_res = compute_dominators(
            nodes=nodes,
            successors=predecessors,
            predecessors=successors,
            entry=single_exit,
        )
        return PostDominatorResult(
            ipdom=dom_res.idom,
            post_dom_tree=dom_res.dom_tree,
            reaches_exit=dom_res.reachable_nodes,
            dead_ends=dom_res.unreachable_nodes,
        )

    virtual_exit: Any = "__VIRTUAL_EXIT__"
    extended_nodes = list(node_set) + [virtual_exit]

    def rev_successors(u: Any) -> Iterable[Any]:
        if u == virtual_exit:
            return exit_list
        return predecessors(u)

    def rev_predecessors(u: Any) -> Iterable[Any]:
        if u == virtual_exit:
            return []
        preds = list(successors(u))
        if u in exit_list:
            preds.append(virtual_exit)
        return preds

    dom_res = compute_dominators(
        nodes=extended_nodes,
        successors=rev_successors,
        predecessors=rev_predecessors,
        entry=virtual_exit,
    )

    reaches_exit = {n for n in dom_res.reachable_nodes if n != virtual_exit}
    dead_ends = node_set - reaches_exit

    ipdom: Dict[T, Optional[T]] = {}
    post_dom_tree: Dict[T, List[T]] = {n: [] for n in reaches_exit}

    for n in reaches_exit:
        parent = dom_res.idom.get(n)
        if parent == virtual_exit:
            ipdom[n] = None
        else:
            ipdom[n] = parent
            if parent is not None and parent in post_dom_tree:
                post_dom_tree[parent].append(n)

    return PostDominatorResult(
        ipdom=ipdom,
        post_dom_tree=post_dom_tree,
        reaches_exit=reaches_exit,
        dead_ends=dead_ends,
    )
