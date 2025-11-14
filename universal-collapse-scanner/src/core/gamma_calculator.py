"""
Gamma (Γ) Calculator - Resilience Coefficient
Measures system's ability to absorb and recover from shock

Γ = (adaptive_capacity + reserves + social_cohesion) / 3

Where values range 0.0-1.0, higher = more resilient
"""

from typing import Dict
from dataclasses import dataclass

@dataclass
class GammaComponents:
    """Resilience factors for Γ calculation"""
    adaptive_capacity: float  # 0.0-1.0 (ability to adapt)
    reserves: float  # 0.0-1.0 (resource reserves)
    social_cohesion: float  # 0.0-1.0 (community strength)

    def __post_init__(self):
        """Validate all components are in range [0, 1]"""
        for field, value in self.__dict__.items():
            if not 0.0 <= value <= 1.0:
                raise ValueError(f"{field} must be between 0.0 and 1.0, got {value}")

class GammaCalculator:
    """Calculate Resilience Coefficient"""

    # Thresholds
    LOW_RESILIENCE = 0.30
    MODERATE_RESILIENCE = 0.50
    HIGH_RESILIENCE = 0.70

    def calculate(self, components: GammaComponents) -> float:
        """
        Calculate Γ resilience coefficient

        Returns:
            float: Γ value (0.0-1.0, higher = more resilient)
        """
        gamma = (
            components.adaptive_capacity +
            components.reserves +
            components.social_cohesion
        ) / 3.0

        return round(gamma, 3)

    def get_status(self, gamma: float) -> str:
        """Get resilience status label"""
        if gamma < self.LOW_RESILIENCE:
            return "LOW_RESILIENCE"
        elif gamma < self.MODERATE_RESILIENCE:
            return "MODERATE_RESILIENCE"
        elif gamma < self.HIGH_RESILIENCE:
            return "HIGH_RESILIENCE"
        else:
            return "VERY_HIGH_RESILIENCE"

    def analyze(self, components: GammaComponents) -> Dict:
        """
        Full Γ analysis

        Returns:
            Dict with gamma value, status, and component breakdown
        """
        gamma = self.calculate(components)
        status = self.get_status(gamma)

        return {
            'gamma': gamma,
            'status': status,
            'components': {
                'adaptive_capacity': components.adaptive_capacity,
                'reserves': components.reserves,
                'social_cohesion': components.social_cohesion
            }
        }
