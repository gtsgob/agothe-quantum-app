"""
Unit tests for Delta Calculator
"""

import unittest
from src.core.delta_calculator import DeltaCalculator, DeltaComponents, ComponentScoring

class TestDeltaCalculator(unittest.TestCase):
    """Test suite for DeltaCalculator"""

    def setUp(self):
        """Set up test fixtures"""
        self.calc = DeltaCalculator()

    def test_calculate_stable(self):
        """Test calculation for stable scenario"""
        components = DeltaComponents(
            severity=0.3,
            irreversibility=0.3,
            time_pressure=0.3,
            response_capacity=0.5,
            recovery_potential=0.5
        )

        delta = self.calc.calculate(components)
        self.assertLess(delta, self.calc.STABLE)

    def test_calculate_critical(self):
        """Test calculation for critical scenario"""
        components = DeltaComponents(
            severity=0.9,
            irreversibility=0.9,
            time_pressure=0.9,
            response_capacity=0.9,
            recovery_potential=0.9
        )

        delta = self.calc.calculate(components)
        self.assertGreater(delta, self.calc.MODERATE)

    def test_component_validation(self):
        """Test that invalid components raise ValueError"""
        with self.assertRaises(ValueError):
            DeltaComponents(
                severity=1.5,  # Invalid
                irreversibility=0.5,
                time_pressure=0.5,
                response_capacity=0.5,
                recovery_potential=0.5
            )

    def test_get_status(self):
        """Test status label assignment"""
        self.assertEqual(self.calc.get_status(0.3), "STABLE")
        self.assertEqual(self.calc.get_status(0.5), "MODERATE_RISK")
        self.assertEqual(self.calc.get_status(0.7), "CRITICAL")
        self.assertEqual(self.calc.get_status(0.9), "CATASTROPHIC")

    def test_analyze_returns_dict(self):
        """Test that analyze returns proper dict structure"""
        components = DeltaComponents(
            severity=0.5,
            irreversibility=0.5,
            time_pressure=0.5,
            response_capacity=0.5,
            recovery_potential=0.5
        )

        result = self.calc.analyze(components)

        self.assertIn('delta', result)
        self.assertIn('status', result)
        self.assertIn('components', result)
        self.assertIn('breakdown', result)

class TestComponentScoring(unittest.TestCase):
    """Test suite for ComponentScoring"""

    def test_severity_humanitarian(self):
        """Test humanitarian severity scoring"""
        score = ComponentScoring.severity_humanitarian(
            deaths_per_day=100,
            displaced=1_000_000,
            food_insecure=5_000_000
        )

        self.assertGreaterEqual(score, 0.0)
        self.assertLessEqual(score, 1.0)

    def test_irreversibility_days(self):
        """Test irreversibility scoring"""
        self.assertEqual(ComponentScoring.irreversibility_days_to_permanent_harm(0), 1.0)
        self.assertEqual(ComponentScoring.irreversibility_days_to_permanent_harm(2), 0.8)
        self.assertEqual(ComponentScoring.irreversibility_days_to_permanent_harm(5), 0.6)

    def test_time_pressure_rate(self):
        """Test time pressure scoring"""
        self.assertEqual(ComponentScoring.time_pressure_rate('chronic'), 0.2)
        self.assertEqual(ComponentScoring.time_pressure_rate('imminent'), 1.0)

if __name__ == '__main__':
    unittest.main()
