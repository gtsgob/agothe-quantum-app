"""
Shared component models
"""

from dataclasses import dataclass
from typing import Dict, Any

@dataclass
class ComponentSet:
    """Generic component set for calculations"""
    components: Dict[str, float]
    metadata: Dict[str, Any] = None

    def __post_init__(self):
        if self.metadata is None:
            self.metadata = {}

    def validate_range(self, min_val: float = 0.0, max_val: float = 1.0):
        """Validate all components are in specified range"""
        for name, value in self.components.items():
            if not min_val <= value <= max_val:
                raise ValueError(
                    f"Component '{name}' value {value} outside range [{min_val}, {max_val}]"
                )
