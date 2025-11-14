"""
Universal Collapse Coefficient (δ) Calculator
Measures system destabilization rate across humanitarian, political,
or mathematical domains.

Formula: δ = (S × I × T) / (R × P)
Where:
  S = Severity (0.0-1.0)
  I = Irreversibility (0.0-1.0)
  T = Time Pressure (0.0-1.0)
  R = Response Capacity (0.0-1.0, inverse)
  P = Recovery Potential (0.0-1.0, inverse)
"""

from typing import Dict, Optional
from dataclasses import dataclass

@dataclass
class DeltaComponents:
    """Components for δ calculation"""
    severity: float  # 0.0-1.0
    irreversibility: float  # 0.0-1.0
    time_pressure: float  # 0.0-1.0
    response_capacity: float  # 0.0-1.0 (higher = worse δ)
    recovery_potential: float  # 0.0-1.0 (higher = worse δ)

    def __post_init__(self):
        """Validate all components are in range [0, 1]"""
        for field, value in self.__dict__.items():
            if not 0.0 <= value <= 1.0:
                raise ValueError(f"{field} must be between 0.0 and 1.0, got {value}")

class DeltaCalculator:
    """Calculate Universal Collapse Coefficient"""

    # Thresholds
    STABLE = 0.35
    MODERATE = 0.65
    CRITICAL = 0.85
    CATASTROPHIC = 0.85

    def __init__(self):
        self.history = []

    def calculate(self, components: DeltaComponents) -> float:
        """
        Calculate δ from components

        Returns:
            float: δ value (typically 0.0-1.5, >1.0 indicates runaway collapse)
        """
        numerator = (
            components.severity *
            components.irreversibility *
            components.time_pressure
        )

        denominator = (
            components.response_capacity *
            components.recovery_potential
        )

        # Prevent division by zero
        if denominator < 0.01:
            denominator = 0.01

        delta = numerator / denominator

        self.history.append({
            'delta': delta,
            'components': components
        })

        return delta

    def get_status(self, delta: float) -> str:
        """Get status label for δ value"""
        if delta < self.STABLE:
            return "STABLE"
        elif delta < self.MODERATE:
            return "MODERATE_RISK"
        elif delta < self.CRITICAL:
            return "CRITICAL"
        else:
            return "CATASTROPHIC"

    def analyze(self, components: DeltaComponents) -> Dict:
        """
        Full analysis with δ calculation and status

        Returns:
            Dict with delta, status, and breakdown
        """
        delta = self.calculate(components)
        status = self.get_status(delta)

        return {
            'delta': round(delta, 3),
            'status': status,
            'components': {
                'severity': components.severity,
                'irreversibility': components.irreversibility,
                'time_pressure': components.time_pressure,
                'response_capacity': components.response_capacity,
                'recovery_potential': components.recovery_potential
            },
            'breakdown': {
                'stress_factors': round(
                    components.severity *
                    components.irreversibility *
                    components.time_pressure, 3
                ),
                'mitigation_capacity': round(
                    components.response_capacity *
                    components.recovery_potential, 3
                )
            }
        }


# Component scoring helper functions
class ComponentScoring:
    """Helper methods for scoring individual components"""

    @staticmethod
    def severity_humanitarian(deaths_per_day: int = 0,
                            displaced: int = 0,
                            food_insecure: int = 0) -> float:
        """
        Score severity for humanitarian crisis

        Returns severity score 0.0-1.0 based on scale
        """
        # Deaths per day scoring
        if deaths_per_day >= 10000:
            death_score = 1.0
        elif deaths_per_day >= 1000:
            death_score = 0.8
        elif deaths_per_day >= 100:
            death_score = 0.6
        elif deaths_per_day >= 10:
            death_score = 0.4
        else:
            death_score = 0.2

        # Displacement scoring (millions)
        displaced_m = displaced / 1_000_000
        if displaced_m >= 5:
            displaced_score = 1.0
        elif displaced_m >= 1:
            displaced_score = 0.8
        elif displaced_m >= 0.1:
            displaced_score = 0.6
        else:
            displaced_score = 0.4

        # Food insecurity scoring (millions)
        food_m = food_insecure / 1_000_000
        if food_m >= 10:
            food_score = 1.0
        elif food_m >= 5:
            food_score = 0.8
        elif food_m >= 1:
            food_score = 0.6
        else:
            food_score = 0.4

        # Weighted average
        return round(
            (death_score * 0.4 + displaced_score * 0.3 + food_score * 0.3),
            2
        )

    @staticmethod
    def irreversibility_days_to_permanent_harm(days: int) -> float:
        """
        Score irreversibility based on time until permanent damage

        Args:
            days: Days until irreversible harm occurs

        Returns:
            Irreversibility score 0.0-1.0
        """
        if days < 1:
            return 1.0
        elif days <= 3:
            return 0.8
        elif days <= 7:
            return 0.6
        elif days <= 30:
            return 0.4
        else:
            return 0.2

    @staticmethod
    def time_pressure_rate(rate_label: str) -> float:
        """
        Score time pressure based on deterioration rate

        Args:
            rate_label: One of ['chronic', 'gradual', 'rapid', 'acute', 'imminent']

        Returns:
            Time pressure score 0.0-1.0
        """
        rates = {
            'chronic': 0.2,
            'gradual': 0.4,
            'rapid': 0.6,
            'acute': 0.8,
            'imminent': 1.0
        }
        return rates.get(rate_label.lower(), 0.5)
