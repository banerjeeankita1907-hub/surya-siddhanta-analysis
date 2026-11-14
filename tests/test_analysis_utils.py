import sys
import unittest
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "code"))
from analysis_utils import angular_residual_deg, summarize_residuals


class AngularResidualTests(unittest.TestCase):
    def test_wraps_across_zero_degrees(self):
        residual = angular_residual_deg(np.array([359.0, 1.0]), np.array([1.0, 359.0]))
        np.testing.assert_allclose(residual, np.array([-2.0, 2.0]))

    def test_residuals_are_in_half_open_interval(self):
        values = angular_residual_deg(
            np.array([0.0, 180.0, 360.0, 720.0]),
            np.zeros(4),
        )
        self.assertTrue(np.all(values >= -180.0))
        self.assertTrue(np.all(values < 180.0))
        np.testing.assert_allclose(values, np.array([0.0, -180.0, 0.0, 0.0]))

    def test_rejects_shape_mismatch_and_non_finite_values(self):
        with self.assertRaises(ValueError):
            angular_residual_deg([1, 2], [1])
        with self.assertRaises(ValueError):
            angular_residual_deg([float("nan")], [0])

    def test_summary_contains_clear_units_and_count(self):
        result = summarize_residuals(np.array([-2.0, 0.0, 2.0]))
        self.assertEqual(result["count"], 3)
        self.assertAlmostEqual(result["mean_absolute_error_deg"], 4.0 / 3.0)
        self.assertAlmostEqual(result["maximum_absolute_error_deg"], 2.0)

    def test_summary_rejects_empty_input(self):
        with self.assertRaises(ValueError):
            summarize_residuals([])


if __name__ == "__main__":
    unittest.main()
