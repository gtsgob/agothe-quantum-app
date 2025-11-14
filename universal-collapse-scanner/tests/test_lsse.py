"""
Unit tests for LSSE Calculator
"""

import unittest
from src.core.lsse_calculator import LSSECalculator, MediaCoverage

class TestLSSECalculator(unittest.TestCase):
    """Test suite for LSSECalculator"""

    def setUp(self):
        """Set up test fixtures"""
        self.calc = LSSECalculator()

    def test_calculate_adequate_coverage(self):
        """Test calculation for adequate coverage"""
        coverage = MediaCoverage(
            actual_articles=10000,
            expected_articles=10000
        )

        lsse = self.calc.calculate(coverage)
        self.assertEqual(lsse, 1.0)

    def test_calculate_suppression(self):
        """Test calculation for suppressed coverage"""
        coverage = MediaCoverage(
            actual_articles=1000,
            expected_articles=10000
        )

        lsse = self.calc.calculate(coverage)
        self.assertEqual(lsse, 0.1)

    def test_zero_expected_raises_error(self):
        """Test that zero expected coverage raises ValueError"""
        coverage = MediaCoverage(
            actual_articles=100,
            expected_articles=0
        )

        with self.assertRaises(ValueError):
            self.calc.calculate(coverage)

    def test_get_status(self):
        """Test status label assignment"""
        self.assertEqual(self.calc.get_status(0.1), "EXTREME_SUPPRESSION")
        self.assertEqual(self.calc.get_status(0.2), "HIGH_SUPPRESSION")
        self.assertEqual(self.calc.get_status(0.4), "MODERATE_SUPPRESSION")
        self.assertEqual(self.calc.get_status(0.6), "ADEQUATE_COVERAGE")

    def test_analyze_returns_dict(self):
        """Test that analyze returns proper dict structure"""
        coverage = MediaCoverage(
            actual_articles=3000,
            expected_articles=10000
        )

        result = self.calc.analyze(coverage)

        self.assertIn('lsse', result)
        self.assertIn('status', result)
        self.assertIn('coverage_gap', result)
        self.assertIn('gap_percentage', result)

    def test_estimate_expected_coverage(self):
        """Test expected coverage estimation"""
        expected = LSSECalculator.estimate_expected_coverage(
            severity_deaths=100000,
            displacement=10_000_000,
            baseline_crisis='ukraine'
        )

        self.assertGreater(expected, 0)
        self.assertIsInstance(expected, int)

if __name__ == '__main__':
    unittest.main()
