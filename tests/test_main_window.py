import unittest
from PyQt6.QtWidgets import QApplication
from ui.windows.user_interface import MainWindow

class TestMainWindow(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.app = QApplication([])

    def setUp(self):
        self.main_window = MainWindow()

    def register_button_opens_registration_window(self):
        self.main_window.register_button.click()
        self.assertTrue(self.main_window.registration_window.isVisible())

    def login_button_opens_login_window(self):
        self.main_window.login_button.click()
        self.assertTrue(self.main_window.login_window.isVisible())

    def main_window_title_is_correct(self):
        self.assertEqual(self.main_window.windowTitle(), "Welcome")

    def main_window_geometry_is_correct(self):
        self.assertEqual(self.main_window.geometry().getRect(), (300, 300, 300, 200))

if __name__ == "__main__":
    unittest.main()
