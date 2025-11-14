"""
Unit tests for Gamma Calculator
"""

import unittest
from src.core.gamma_calculator import GammaCalculator, GammaComponents

class TestGammaCalculator(unittest.TestCase):
    """Test suite for GammaCalculator"""

    def setUp(self):
        """Set up test fixtures"""
        self.calc = GammaCalculator()

    def test_calculate_high_resilience(self):
        """Test calculation for high resilience"""
        components = GammaComponents(
            adaptive_capacity=0.8,
            reserves=0.8,
            social_cohesion=0.8
        )

        gamma = self.calc.calculate(components)
        self.assertGreaterEqual(gamma, self.calc.HIGH_RESILIENCE)

    def test_calculate_low_resilience(self):
        """Test calculation for low resilience"""
        components = GammaComponents(
            adaptive_capacity=0.2,
            reserves=0.2,
            social_cohesion=0.2
        )

        gamma = self.calc.calculate(components)
        self.assertLess(gamma, self.calc.MODERATE_RESILIENCE)

    def test_component_validation(self):
        """Test that invalid components raise ValueError"""
        with self.assertRaises(ValueError):
            GammaComponents(
                adaptive_capacity=-0.1,  # Invalid
                reserves=0.5,
                social_cohesion=0.5
            )

    def test_get_status(self):
        """Test status label assignment"""
        self.assertEqual(self.calc.get_status(0.2), "LOW_RESILIENCE")
        self.assertEqual(self.calc.get_status(0.4), "MODERATE_RESILIENCE")
        self.assertEqual(self.calc.get_status(0.6), "HIGH_RESILIENCE")
        self.assertEqual(self.calc.get_status(0.8), "VERY_HIGH_RESILIENCE")

    def test_analyze_returns_dict(self):
        """Test that analyze returns proper dict structure"""
        components = GammaComponents(
            adaptive_capacity=0.5,
            reserves=0.5,
            social_cohesion=0.5
        )

        result = self.calc.analyze(components)

        self.assertIn('gamma', result)
        self.assertIn('status', result)
        self.assertIn('components', result)

if __name__ == '__main__':
    unittest.main()
