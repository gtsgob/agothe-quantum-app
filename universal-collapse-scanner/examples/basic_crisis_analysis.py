"""
Basic Crisis Analysis Example
Demonstrates core scanner functionality
"""

from src.core.delta_calculator import DeltaCalculator, DeltaComponents, ComponentScoring
from src.core.lsse_calculator import LSSECalculator, MediaCoverage
from src.core.geometry_router import GeometryRouter, Geometry

def analyze_humanitarian_crisis():
    """Example: Analyze a humanitarian crisis"""

    print("=" * 60)
    print("UNIVERSAL COLLAPSE SCANNER - Basic Analysis")
    print("=" * 60)

    # Step 1: Calculate δ (Collapse Coefficient)
    print("\n1. CALCULATING COLLAPSE COEFFICIENT (δ)\n")

    scorer = ComponentScoring()

    # Score components
    severity = scorer.severity_humanitarian(
        deaths_per_day=150,
        displaced=14_000_000,
        food_insecure=25_000_000
    )

    irreversibility = scorer.irreversibility_days_to_permanent_harm(days=7)
    time_pressure = scorer.time_pressure_rate('acute')

    components = DeltaComponents(
        severity=severity,
        irreversibility=irreversibility,
        time_pressure=time_pressure,
        response_capacity=0.90,  # Very limited response (inverse scale)
        recovery_potential=0.85   # Very low recovery potential (inverse scale)
    )

    delta_calc = DeltaCalculator()
    analysis = delta_calc.analyze(components)

    print(f"δ Score: {analysis['delta']} ({analysis['status']})")
    print(f"\nComponent Breakdown:")
    for component, value in analysis['components'].items():
        print(f"  {component}: {value}")

    # Step 2: Calculate LSSE (Media Suppression)
    print("\n2. CALCULATING MEDIA SUPPRESSION (LSSE)\n")

    coverage = MediaCoverage(
        actual_articles=1400,
        expected_articles=12000,
        timeframe_days=30
    )

    lsse_calc = LSSECalculator()
    lsse_analysis = lsse_calc.analyze(coverage)

    print(f"LSSE Score: {lsse_analysis['lsse']} ({lsse_analysis['status']})")
    print(f"Coverage Gap: {lsse_analysis['coverage_gap']} articles")
    print(f"Gap Percentage: {lsse_analysis['gap_percentage']}% under-covered")

    # Step 3: Route to Geometries
    print("\n3. IDENTIFYING CONSTRAINT GEOMETRIES\n")

    crisis_patterns = {
        'blockade': True,
        'siege': True,
        'displacement': True,
        'inequality': True,
        'hidden_actors': True
    }

    router = GeometryRouter()
    geometries = router.route(crisis_patterns)

    print(f"Identified {len(geometries)} primary geometries:")
    for i, geometry in enumerate(geometries, 1):
        print(f"  {i}. {geometry.name}: {router.describe_geometry(geometry)}")

    # Step 4: Summary
    print("\n" + "=" * 60)
    print("SUMMARY")
    print("=" * 60)
    print(f"Collapse Status: {analysis['status']}")
    print(f"Media Suppression: {lsse_analysis['status']}")
    print(f"Primary Geometry: {geometries[0].name if geometries else 'None'}")
    print(f"\nIntervention Priority: {'URGENT' if analysis['delta'] > 0.85 else 'HIGH' if analysis['delta'] > 0.65 else 'MODERATE'}")
    print("=" * 60)

if __name__ == "__main__":
    analyze_humanitarian_crisis()
