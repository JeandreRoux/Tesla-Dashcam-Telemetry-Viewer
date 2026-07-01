import os
import unittest
from pathlib import Path

from modules import app_service, layouts


os.environ.setdefault("QT_QPA_PLATFORM", "offscreen")


try:
    import desktop_ui
except ImportError as error:  # pragma: no cover - only used when optional UI deps are absent locally
    desktop_ui = None
    IMPORT_ERROR = error
else:
    IMPORT_ERROR = None


@unittest.skipIf(desktop_ui is None, f"desktop UI dependencies unavailable: {IMPORT_ERROR}")
class TestDesktopUiLayoutState(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        assert desktop_ui is not None
        try:
            cls.qt = desktop_ui._load_qt()
        except ImportError as error:
            raise unittest.SkipTest(f"desktop UI dependencies unavailable: {error}") from error
        cls.QApplication = cls.qt["QApplication"]
        cls.app = cls.QApplication.instance() or cls.QApplication([])
        cls.MainWindow = desktop_ui.create_main_window(cls.qt)

    def tearDown(self):
        for widget in self.app.topLevelWidgets():
            widget.close()

    def test_launch_does_not_show_default_layout_before_input_scan(self):
        window = self.MainWindow()

        self.assertEqual(window.layout_combo.count(), 0)
        self.assertEqual(window.layout_combo.currentText(), "")
        self.assertEqual(window.layout_combo.placeholderText(), "Automatic layout")
        self.assertIn("Camera layout", window.diagram_label.text())
        self.assertEqual(window.status_label.text(), "Add an input folder to begin.")
        self.assertEqual(window.layout_combo.toolTip(), "")
        self.assertEqual(window.diagram_label.toolTip(), "")
        self.assertFalse(window.render_button.isEnabled())

    def test_scan_result_populates_detected_layout(self):
        window = self.MainWindow()
        window.input_edit.setText("/input")
        window.output_edit.setText("/output")
        scan = app_service.ScanResult(
            input_path=Path("/input"),
            layout=layouts.SIX_CAMERA_DEFAULT,
            camera_set="six-camera",
            clip_group_count=2,
        )

        window._on_scan_finished(scan)
        window._sync_buttons()

        self.assertEqual(window.layout_combo.currentText(), "Six-camera grid")
        self.assertIn("Left pillar", window.diagram_label.text())
        self.assertEqual(window.status_label.text(), "Ready to render.")
        self.assertEqual(window.progress.value(), 0)
        self.assertTrue(window.render_button.isEnabled())


if __name__ == "__main__":
    unittest.main()
