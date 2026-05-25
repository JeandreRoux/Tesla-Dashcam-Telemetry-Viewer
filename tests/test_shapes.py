import unittest

from modules.shapes import calculate_fill_angles


class TestCalculateFillAngles(unittest.TestCase):
    def test_zero_percent_returns_bottom_angle(self):
        start_angle, end_angle = calculate_fill_angles(0)

        self.assertEqual(start_angle, 90)
        self.assertEqual(end_angle, 90)

    def test_full_percent_returns_full_circle_angles(self):
        start_angle, end_angle = calculate_fill_angles(100)

        self.assertEqual(start_angle, -90)
        self.assertEqual(end_angle, 270)

    def test_negative_percent_is_clamped_to_zero(self):
        start_angle, end_angle = calculate_fill_angles(-10)

        self.assertEqual(start_angle, 90)
        self.assertEqual(end_angle, 90)

    def test_percent_over_100_is_clamped_to_100(self):
        start_angle, end_angle = calculate_fill_angles(140)

        self.assertEqual(start_angle, -90)
        self.assertEqual(end_angle, 270)


if __name__ == "__main__":
    unittest.main()
