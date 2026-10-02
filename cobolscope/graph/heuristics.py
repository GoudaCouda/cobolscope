"""
cobolscope.graph.heuristics
~~~~~~~~~~~~~~~~~~~~~~~~~~~

Dynamic topology analysis and layout heuristics for Procedure Call Graphs.
Calculates mathematical graph invariants to automatically tune layout spacing,
ranker algorithms, and engine recommendations for large graphs (50 to 200+ routines).
"""

from __future__ import annotations
from dataclasses import dataclass
from typing import Dict, List, Optional, Set
from collections import defaultdict, deque

from .models import CallGraph, CallGraphNode, GraphEdgeType


@dataclass
class GraphMetrics:
    """Mathematical graph topology metrics calculated from a CallGraph."""
    total_nodes: int
    total_edges: int
    density: float
    avg_degree: float
    max_in_degree: int
    max_out_degree: int
    max_rank_width: int
    hierarchy_depth: int
    aspect_ratio: float
    scale_category: str  # "small", "medium", "large", "massive"
    high_indegree_nodes: List[str]

    def to_dict(self) -> Dict[str, Any]:
        from dataclasses import asdict
        return asdict(self)


@dataclass
class LayoutHeuristics:
    """Dynamically computed layout parameters for Graphviz, Dagre, and ELK."""
    ranker: str             # "network-simplex" | "tight-tree" | "longest-path"
    nodesep_in: float       # Graphviz nodesep (inches)
    ranksep_in: float       # Graphviz ranksep (inches)
    cyto_nodesep: int       # Cytoscape Dagre/ELK node separation (px)
    cyto_ranksep: int       # Cytoscape Dagre/ELK rank separation (px)
    splines: str            # "ortho" | "spline" | "polyline"
    recommend_elk: bool     # True if ELK should be recommended/defaulted
    recommend_cloning: bool # True if node cloning would significantly disentangle the graph
    summary_label: str      # Human-readable summary for UI telemetry/badges

    def to_dict(self) -> Dict[str, Any]:
        from dataclasses import asdict
        return asdict(self)



def compute_graph_metrics(graph: CallGraph) -> GraphMetrics:
    """
    Computes topological invariants and rank distribution for a CallGraph.

    Args:
        graph: The CallGraph to inspect.

    Returns:
        GraphMetrics containing calculated topological statistics.
    """
    n = len(graph.nodes)
    e = len(graph.edges)

    if n == 0:
        return GraphMetrics(
            total_nodes=0,
            total_edges=0,
            density=0.0,
            avg_degree=0.0,
            max_in_degree=0,
            max_out_degree=0,
            max_rank_width=0,
            hierarchy_depth=0,
            aspect_ratio=1.0,
            scale_category="small",
            high_indegree_nodes=[],
        )

    # In-degree and Out-degree calculation
    in_degrees: Dict[str, int] = defaultdict(int)
    out_degrees: Dict[str, int] = defaultdict(int)

    for edge in graph.edges:
        if edge.source in graph.nodes and edge.target in graph.nodes:
            out_degrees[edge.source] += 1
            in_degrees[edge.target] += 1

    max_in = max(in_degrees.values()) if in_degrees else 0
    max_out = max(out_degrees.values()) if out_degrees else 0
    avg_deg = round(e / n, 2)
    density = round(e / (n * (n - 1)), 4) if n > 1 else 0.0

    # High in-degree utility routines (in-degree >= 3)
    high_indegree = [
        name for name, deg in in_degrees.items()
        if deg >= 3 and name in graph.nodes and not graph.nodes[name].is_entry_point
    ]
    high_indegree.sort(key=lambda k: in_degrees[k], reverse=True)

    # Approximate topological layering / rank depth using longest path DAG layering
    # (ignoring cycle back-edges)
    ranks: Dict[str, int] = {}
    entry = graph.entry_point if graph.entry_point and graph.entry_point in graph.nodes else None

    # Construct forward adjacency excluding backward/cycle edges
    adj: Dict[str, List[str]] = defaultdict(list)
    for edge in graph.edges:
        if edge.source in graph.nodes and edge.target in graph.nodes:
            # Don't add self loops
            if edge.source != edge.target:
                adj[edge.source].append(edge.target)

    # BFS/Longest-path layering starting from entry point or all roots
    roots = [name for name in graph.nodes if in_degrees[name] == 0]
    if entry and entry not in roots:
        roots.insert(0, entry)
    if not roots:
        roots = list(graph.nodes.keys())[:1]

    # Topological level assignment
    queue = deque()
    for r in roots:
        ranks[r] = 0
        queue.append(r)

    visited_count: Dict[str, int] = defaultdict(int)
    max_queue_iters = n * 4
    iters = 0

    while queue and iters < max_queue_iters:
        iters += 1
        curr = queue.popleft()
        curr_rank = ranks[curr]
        for neighbor in adj[curr]:
            new_rank = curr_rank + 1
            if neighbor not in ranks or new_rank > ranks[neighbor]:
                ranks[neighbor] = new_rank
                visited_count[neighbor] += 1
                if visited_count[neighbor] < 5:  # prevent infinite loop in cycles
                    queue.append(neighbor)

    # Assign rank 0 to any unvisited nodes
    for name in graph.nodes:
        if name not in ranks:
            ranks[name] = 0

    hierarchy_depth = max(ranks.values()) + 1 if ranks else 1

    # Calculate width per rank
    rank_counts: Dict[int, int] = defaultdict(int)
    for r in ranks.values():
        rank_counts[r] += 1

    max_rank_width = max(rank_counts.values()) if rank_counts else 1
    aspect_ratio = round(max_rank_width / max(hierarchy_depth, 1), 2)

    # Scale category
    if n <= 25:
        scale_cat = "small"
    elif n <= 75:
        scale_cat = "medium"
    elif n <= 150:
        scale_cat = "large"
    else:
        scale_cat = "massive"

    return GraphMetrics(
        total_nodes=n,
        total_edges=e,
        density=density,
        avg_degree=avg_deg,
        max_in_degree=max_in,
        max_out_degree=max_out,
        max_rank_width=max_rank_width,
        hierarchy_depth=hierarchy_depth,
        aspect_ratio=aspect_ratio,
        scale_category=scale_cat,
        high_indegree_nodes=high_indegree,
    )


def calculate_layout_heuristics(
    metrics: GraphMetrics,
    compact_nodes: bool = True,
    requested_splines: Optional[str] = None,
    requested_ranker: Optional[str] = None,
) -> LayoutHeuristics:
    """
    Derives optimal layout parameters from graph metrics.

    Args:
        metrics: Computed GraphMetrics.
        compact_nodes: Whether node boxes are compact or detailed.
        requested_splines: Optional user-requested spline style override.
        requested_ranker: Optional user-requested ranker override.

    Returns:
        LayoutHeuristics specifying optimal engine arguments and spacing.
    """
    n = metrics.total_nodes

    # 1. Ranker Selection
    # network-simplex: Best for small graphs (tight edge lengths)
    # tight-tree: Fast, prevents runaway simplex iterations on medium/dense graphs
    # longest-path: Best for deep hierarchies or wide branches to pull callers/callees together
    if requested_ranker:
        ranker = requested_ranker
    elif n <= 35:
        ranker = "network-simplex"
    elif n <= 85 and metrics.density <= 0.08:
        ranker = "tight-tree"
    else:
        ranker = "longest-path"

    # 2. Vertical Rank Separation (ranksep)
    # Scales inversely with node count to avoid massive vertical scrolling on 100+ node graphs
    if n <= 25:
        ranksep_in = 0.75
        cyto_ranksep = 60
    elif n <= 75:
        ranksep_in = 0.60
        cyto_ranksep = 50
    elif n <= 150:
        ranksep_in = 0.48
        cyto_ranksep = 42
    else:
        ranksep_in = 0.38
        cyto_ranksep = 34

    # Aspect ratio adjustment: If diagram is extremely tall (spaghetti ladder), compress vertical spacing
    if metrics.aspect_ratio < 0.6 and n > 20:
        ranksep_in = max(0.32, round(ranksep_in * 0.85, 2))
        cyto_ranksep = max(28, int(cyto_ranksep * 0.85))
    # If diagram is very wide, give slightly more vertical breathing room for routing trunks
    elif metrics.aspect_ratio > 1.8:
        ranksep_in = min(0.85, round(ranksep_in * 1.15, 2))
        cyto_ranksep = min(75, int(cyto_ranksep * 1.15))

    # 3. Horizontal Node Separation (nodesep)
    # Wider when max rank width or density is high to prevent parallel vertical edge collision
    if metrics.max_rank_width <= 8:
        nodesep_in = 0.45
        cyto_nodesep = 45
    elif metrics.max_rank_width <= 16:
        nodesep_in = 0.55
        cyto_nodesep = 55
    else:
        nodesep_in = 0.70
        cyto_nodesep = 70

    if not compact_nodes:
        # Detailed nodes with variable lineage require more horizontal margin
        nodesep_in = round(nodesep_in + 0.15, 2)
        cyto_nodesep += 15

    # 4. Splines (Edge Routing Style)
    if requested_splines:
        splines = requested_splines
    else:
        # Default to standard spline; Graphviz ortho routing frequently freezes on clustered graphs
        splines = "spline"


    # 5. Engine & Cloning Recommendations
    recommend_elk = n >= 35
    recommend_cloning = len(metrics.high_indegree_nodes) >= 2 or metrics.max_in_degree >= 5

    summary_label = (
        f"{metrics.scale_category.upper()} ({n} routines, {metrics.total_edges} calls | "
        f"Ranker: {ranker}, ranksep: {ranksep_in}\", nodesep: {nodesep_in}\")"
    )

    return LayoutHeuristics(
        ranker=ranker,
        nodesep_in=nodesep_in,
        ranksep_in=ranksep_in,
        cyto_nodesep=cyto_nodesep,
        cyto_ranksep=cyto_ranksep,
        splines=splines,
        recommend_elk=recommend_elk,
        recommend_cloning=recommend_cloning,
        summary_label=summary_label,
    )
