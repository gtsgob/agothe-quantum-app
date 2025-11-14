"""
Threshold definitions for various metrics
"""

from dataclasses import dataclass
from typing import Dict, List, Tuple

@dataclass
class ThresholdSet:
    """Defines thresholds for a metric"""
    metric_name: str
    thresholds: List[Tuple[float, str]]  # (threshold_value, label)

    def get_status(self, value: float) -> str:
        """Get status label for a given value"""
        # Sort thresholds in ascending order
        sorted_thresholds = sorted(self.thresholds, key=lambda x: x[0])

        for threshold, label in sorted_thresholds:
            if value < threshold:
                return label

        # If value exceeds all thresholds, return last label
        return sorted_thresholds[-1][1] if sorted_thresholds else "UNKNOWN"


# Standard threshold sets
DELTA_THRESHOLDS = ThresholdSet(
    metric_name="delta",
    thresholds=[
        (0.35, "STABLE"),
        (0.65, "MODERATE_RISK"),
        (0.85, "CRITICAL"),
        (float('inf'), "CATASTROPHIC")
    ]
)

LSSE_THRESHOLDS = ThresholdSet(
    metric_name="lsse",
    thresholds=[
        (0.15, "EXTREME_SUPPRESSION"),
        (0.30, "HIGH_SUPPRESSION"),
        (0.50, "MODERATE_SUPPRESSION"),
        (float('inf'), "ADEQUATE_COVERAGE")
    ]
)

GAMMA_THRESHOLDS = ThresholdSet(
    metric_name="gamma",
    thresholds=[
        (0.30, "LOW_RESILIENCE"),
        (0.50, "MODERATE_RESILIENCE"),
        (0.70, "HIGH_RESILIENCE"),
        (float('inf'), "VERY_HIGH_RESILIENCE")
    ]
)
