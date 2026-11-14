import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "code"))
from surya_siddhanta import ahargaña, mean_longitude, manda_phala, true_longitude


class SimplifiedModelTests(unittest.TestCase):
    def test_kaliyuga_epoch_has_zero_elapsed_days(self):
        self.assertAlmostEqual(ahargaña(588465.5), 0.0)

    def test_mean_longitude_is_periodic_modulo_360(self):
        days = 1234.5
        for planet, motion in [
            ("sun", 0.985602),
            ("moon", 13.176352),
            ("mars", 0.524033),
        ]:
            a = mean_longitude(planet, days)
            b = mean_longitude(planet, days + 360.0 / motion)
            self.assertAlmostEqual(a, b, places=8)

    def test_manda_term_is_small_and_finite(self):
        correction = manda_phala("mars", 45.0)
        self.assertTrue(abs(correction) <= 73.0 / 360.0 + 1e-12)

    def test_true_longitude_is_normalized(self):
        for planet in ["sun", "moon", "mercury", "venus", "mars", "jupiter", "saturn"]:
            longitude = true_longitude(planet, 2451545.0)
            self.assertTrue(0.0 <= longitude < 360.0)


if __name__ == "__main__":
    unittest.main()
