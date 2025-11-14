"""
Geometry Mapping Example
Demonstrates crisis pattern routing to mathematical geometries
"""

from src.core.geometry_router import GeometryRouter, Geometry

def analyze_crisis_geometries():
    """Analyze different crisis types and their geometries"""

    print("=" * 60)
    print("MILLENNIUM PROCESSOR - Geometry Mapping")
    print("=" * 60)

    router = GeometryRouter()

    # Define different crisis scenarios
    scenarios = [
        {
            'name': 'Siege Warfare Crisis',
            'patterns': {
                'blockade': True,
                'siege': True,
                'confinement': True,
                'displacement': True
            }
        },
        {
            'name': 'Economic Collapse',
            'patterns': {
                'market_disconnect': True,
                'valuation_failure': True,
                'inequality': True,
                'chaos': True
            }
        },
        {
            'name': 'Information Warfare',
            'patterns': {
                'complexity_asymmetry': True,
                'information_warfare': True,
                'hidden_actors': True
            }
        },
        {
            'name': 'Infrastructure Breakdown',
            'patterns': {
                'network_collapse': True,
                'infrastructure_breakdown': True,
                'flow_breakdown': True,
                'logistics_collapse': True
            }
        },
        {
            'name': 'Sudden Regime Change',
            'patterns': {
                'sudden_shift': True,
                'impossible_event': True,
                'tipping_point': True,
                'phase_shift': True
            }
        }
    ]

    print("\nMapping crisis patterns to constraint geometries:\n")

    for scenario in scenarios:
        print(f"\n{scenario['name']}")
        print("-" * 60)

        geometries = router.route(scenario['patterns'])

        if geometries:
            print(f"Matched {len(geometries)} geometries:")
            for i, geometry in enumerate(geometries, 1):
                print(f"  {i}. {geometry.name}")
                print(f"     {router.describe_geometry(geometry)}")
        else:
            print("  No geometries matched")

    # Show all available routing questions
    print("\n" + "=" * 60)
    print("AVAILABLE GEOMETRY ROUTING QUESTIONS")
    print("=" * 60)

    for geometry, question in router.routing_questions.items():
        print(f"\n{geometry.name}:")
        print(f"  Question: {question}")
        print(f"  Description: {router.describe_geometry(geometry)}")

    print("\n" + "=" * 60)

if __name__ == "__main__":
    analyze_crisis_geometries()
