"""
Psi (Ψ) Calculator - Crisis Amplification Factor
Measures how structural factors amplify base crisis severity

Ψ = 1 + (vulnerability × exposure × fragility)

Where values range 0.0-1.0, resulting in Ψ ∈ [1.0, 2.0]
"""

from typing import Dict
from dataclasses import dataclass

@dataclass
class PsiComponents:
    """Amplification factors for Ψ calculation"""
    vulnerability: float  # 0.0-1.0 (population vulnerability)
    exposure: float  # 0.0-1.0 (geographic/economic exposure)
    fragility: float  # 0.0-1.0 (institutional fragility)

    def __post_init__(self):
        """Validate all components are in range [0, 1]"""
        for field, value in self.__dict__.items():
            if not 0.0 <= value <= 1.0:
                raise ValueError(f"{field} must be between 0.0 and 1.0, got {value}")

class PsiCalculator:
    """Calculate Crisis Amplification Factor"""

    def calculate(self, components: PsiComponents) -> float:
        """
        Calculate Ψ amplification factor

        Returns:
            float: Ψ value (1.0-2.0, where 1.0 = no amplification, 2.0 = maximum)
        """
        amplification = (
            components.vulnerability *
            components.exposure *
            components.fragility
        )

        psi = 1.0 + amplification
        return round(psi, 3)

    def analyze(self, components: PsiComponents) -> Dict:
        """
        Full Ψ analysis

        Returns:
            Dict with psi value and component breakdown
        """
        psi = self.calculate(components)

        return {
            'psi': psi,
            'amplification_factor': round(psi - 1.0, 3),
            'components': {
                'vulnerability': components.vulnerability,
                'exposure': components.exposure,
                'fragility': components.fragility
            }
        }
