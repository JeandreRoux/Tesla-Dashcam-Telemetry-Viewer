import unittest

from modules import layouts


FOUR_CAMERA_FILES = {
    "front": "2026-06-19_23-08-01-front.mp4",
    "back": "2026-06-19_23-08-01-back.mp4",
    "left_repeater": "2026-06-19_23-08-01-left_repeater.mp4",
    "right_repeater": "2026-06-19_23-08-01-right_repeater.mp4",
}

SIX_CAMERA_FILES = {
    **FOUR_CAMERA_FILES,
    "left_pillar": "2026-06-19_23-08-01-left_pillar.mp4",
    "right_pillar": "2026-06-19_23-08-01-right_pillar.mp4",
}


class TestSelectDefaultLayout(unittest.TestCase):
    def test_selects_four_camera_layout_for_complete_four_camera_set(self):
        video_data = {"2026-06-19_23-08-01": FOUR_CAMERA_FILES}

        layout = layouts.select_default_layout(video_data)

        self.assertIs(layout, layouts.FOUR_CAMERA_DEFAULT)

    def test_selects_six_camera_layout_for_complete_six_camera_set(self):
        video_data = {"2026-06-19_23-08-01": SIX_CAMERA_FILES}

        layout = layouts.select_default_layout(video_data)

        self.assertIs(layout, layouts.SIX_CAMERA_DEFAULT)

    def test_rejects_mixed_four_and_six_camera_batches(self):
        video_data = {
            "2026-06-19_23-08-01": SIX_CAMERA_FILES,
            "2026-06-19_23-09-01": {
                key: value.replace("23-08-01", "23-09-01")
                for key, value in FOUR_CAMERA_FILES.items()
            },
        }

        with self.assertRaisesRegex(ValueError, "mixed or incomplete"):
            layouts.select_default_layout(video_data)

    def test_rejects_partial_six_camera_set(self):
        partial_six_camera_files = dict(SIX_CAMERA_FILES)
        del partial_six_camera_files["right_pillar"]
        video_data = {"2026-06-19_23-08-01": partial_six_camera_files}

        with self.assertRaisesRegex(ValueError, "right_pillar"):
            layouts.select_default_layout(video_data)

    def test_six_camera_regions_are_equal_size_grid_cells(self):
        regions = layouts.SIX_CAMERA_DEFAULT["regions"]

        self.assertEqual(
            set(regions),
            {
                "left_pillar",
                "front",
                "right_pillar",
                "left_repeater",
                "back",
                "right_repeater",
            },
        )
        self.assertTrue(
            all(width == 426 and height == 360 for _, _, width, height in regions.values())
        )
        self.assertEqual(regions["left_pillar"], (1, 0, 426, 360))
        self.assertEqual(regions["front"], (427, 0, 426, 360))
        self.assertEqual(regions["right_pillar"], (853, 0, 426, 360))


if __name__ == "__main__":
    unittest.main()
