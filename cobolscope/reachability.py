"""
Backward-compatibility proxy for cobolscope.reachability.
"""

from cobolscope.reachability import (
    TransitionKind,
    PerformFrame,
    StateTransition,
    ReachabilityModel,
    PushdownReachabilityAnalyzer,
)

__all__ = [
    "TransitionKind",
    "PerformFrame",
    "StateTransition",
    "ReachabilityModel",
    "PushdownReachabilityAnalyzer",
]
