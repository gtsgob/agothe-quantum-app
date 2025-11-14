"""
LSSE Measurement Example
Demonstrates media suppression analysis
"""

from src.core.lsse_calculator import LSSECalculator, MediaCoverage

def compare_crisis_coverage():
    """Compare media coverage across different crises"""

    print("=" * 60)
    print("LSSE MEASUREMENT - Media Coverage Analysis")
    print("=" * 60)

    calc = LSSECalculator()

    # Define multiple crises for comparison
    crises = [
        {
            'name': 'Crisis A (Major Western Coverage)',
            'coverage': MediaCoverage(
                actual_articles=15000,
                expected_articles=15000,
                timeframe_days=30
            )
        },
        {
            'name': 'Crisis B (Moderate Suppression)',
            'coverage': MediaCoverage(
                actual_articles=4000,
                expected_articles=12000,
                timeframe_days=30
            )
        },
        {
            'name': 'Crisis C (High Suppression)',
            'coverage': MediaCoverage(
                actual_articles=2000,
                expected_articles=10000,
                timeframe_days=30
            )
        },
        {
            'name': 'Crisis D (Extreme Suppression)',
            'coverage': MediaCoverage(
                actual_articles=800,
                expected_articles=12000,
                timeframe_days=30
            )
        }
    ]

    print("\nAnalyzing media coverage patterns:\n")

    for crisis in crises:
        analysis = calc.analyze(crisis['coverage'])

        print(f"{crisis['name']}")
        print(f"  LSSE: {analysis['lsse']}")
        print(f"  Status: {analysis['status']}")
        print(f"  Gap: {analysis['coverage_gap']} articles ({analysis['gap_percentage']}%)")
        print()

    # Demonstrate expected coverage estimation
    print("\n" + "=" * 60)
    print("EXPECTED COVERAGE ESTIMATION")
    print("=" * 60)

    expected = LSSECalculator.estimate_expected_coverage(
        severity_deaths=50000,
        displacement=5_000_000,
        baseline_crisis='ukraine'
    )

    print(f"\nFor a crisis with:")
    print(f"  - 50,000 deaths")
    print(f"  - 5,000,000 displaced")
    print(f"  - Baseline: Ukraine war")
    print(f"\nExpected monthly coverage: {expected} articles")
    print("=" * 60)

if __name__ == "__main__":
    compare_crisis_coverage()
