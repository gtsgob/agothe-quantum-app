"""
Large-Scale Suppression Effect (LSSE) Calculator
Measures media coverage gaps for crises

LSSE = Actual_Coverage / Expected_Coverage

Thresholds:
  < 0.15: Extreme suppression
  0.15-0.30: High suppression
  0.30-0.50: Moderate suppression
  > 0.50: Adequate coverage
"""

from typing import Optional, Dict
from dataclasses import dataclass

@dataclass
class MediaCoverage:
    """Media coverage metrics"""
    actual_articles: int
    expected_articles: int  # Based on comparable crisis
    actual_social_mentions: Optional[int] = None
    expected_social_mentions: Optional[int] = None
    timeframe_days: int = 30

class LSSECalculator:
    """Calculate Large-Scale Suppression Effect"""

    # Thresholds
    EXTREME_SUPPRESSION = 0.15
    HIGH_SUPPRESSION = 0.30
    MODERATE_SUPPRESSION = 0.50

    def calculate(self, coverage: MediaCoverage) -> float:
        """
        Calculate LSSE ratio

        Returns:
            float: LSSE value (0.0-1.0+, typically <1.0 indicates suppression)
        """
        if coverage.expected_articles == 0:
            raise ValueError("Expected coverage cannot be zero")

        lsse = coverage.actual_articles / coverage.expected_articles
        return round(lsse, 3)

    def get_status(self, lsse: float) -> str:
        """Get suppression status label"""
        if lsse < self.EXTREME_SUPPRESSION:
            return "EXTREME_SUPPRESSION"
        elif lsse < self.HIGH_SUPPRESSION:
            return "HIGH_SUPPRESSION"
        elif lsse < self.MODERATE_SUPPRESSION:
            return "MODERATE_SUPPRESSION"
        else:
            return "ADEQUATE_COVERAGE"

    def analyze(self, coverage: MediaCoverage) -> Dict:
        """
        Full LSSE analysis

        Returns:
            Dict with LSSE score, status, and metrics
        """
        lsse = self.calculate(coverage)
        status = self.get_status(lsse)

        analysis = {
            'lsse': lsse,
            'status': status,
            'coverage_gap': coverage.expected_articles - coverage.actual_articles,
            'gap_percentage': round((1 - lsse) * 100, 1),
            'timeframe_days': coverage.timeframe_days
        }

        # Add social media metrics if available
        if coverage.actual_social_mentions and coverage.expected_social_mentions:
            social_lsse = coverage.actual_social_mentions / coverage.expected_social_mentions
            analysis['social_lsse'] = round(social_lsse, 3)

        return analysis

    @staticmethod
    def estimate_expected_coverage(severity_deaths: int,
                                   displacement: int,
                                   baseline_crisis: str = "ukraine") -> int:
        """
        Estimate expected coverage based on comparable crisis

        Args:
            severity_deaths: Total deaths
            displacement: Total displaced
            baseline_crisis: Comparable crisis for scaling

        Returns:
            Estimated monthly article count
        """
        # Baseline: Ukraine war ~15,000 articles/month at peak
        # with ~100K deaths, ~10M displaced

        baselines = {
            'ukraine': {'articles': 15000, 'deaths': 100000, 'displaced': 10_000_000},
            'gaza': {'articles': 12000, 'deaths': 50000, 'displaced': 2_000_000}
        }

        base = baselines.get(baseline_crisis, baselines['ukraine'])

        # Scale by severity (deaths + displacement)
        severity_ratio = (
            (severity_deaths / base['deaths']) * 0.6 +
            (displacement / base['displaced']) * 0.4
        )

        estimated = int(base['articles'] * severity_ratio)
        return max(estimated, 100)  # Minimum 100 articles/month for any crisis
