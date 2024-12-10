import unittest
from unittest.mock import patch
from PyQt6.QtWidgets import QMessageBox, QApplication
from ui.windows.registration import RegistrationWindow

class TestRegistrationWindow(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.app = QApplication([])

    def test_registration_window_title_is_correct(self):
        registration_window = RegistrationWindow()
        self.assertEqual(registration_window.windowTitle(), "Register")

    def test_registration_window_geometry_is_correct(self):
        registration_window = RegistrationWindow()
        self.assertEqual(registration_window.geometry().getRect(), (350, 350, 300, 200))

    def test_register_user_with_valid_data_shows_success_message(self):
        registration_window = RegistrationWindow()
        registration_window.username_input.setText("validuser")
        registration_window.password_input.setText("validpassword")
        with patch('database.database.add_user', return_value="User added successfully"):
            with patch.object(QMessageBox, 'information') as mock_info:
                registration_window.register_button.click()
                mock_info.assert_called_once_with(registration_window, "Success", "User added successfully")

    def test_register_user_with_empty_fields_shows_error_message(self):
        registration_window = RegistrationWindow()
        registration_window.username_input.setText("")
        registration_window.password_input.setText("")
        with patch.object(QMessageBox, 'warning') as mock_warning:
            registration_window.register_button.click()
            mock_warning.assert_called_once_with(registration_window, "Error", "Please fill out all fields.")

    def test_register_user_with_existing_username_shows_error_message(self):
        registration_window = RegistrationWindow()
        registration_window.username_input.setText("existinguser")
        registration_window.password_input.setText("validpassword")
        with patch('database.database.add_user', return_value="Username already exists"):
            with patch.object(QMessageBox, 'warning') as mock_warning:
                registration_window.register_button.click()
                mock_warning.assert_called_once_with(registration_window, "Error", "Username already exists")

    @classmethod
    def tearDownClass(cls):
        cls.app.quit()


if __name__ == '__main__':
    # app = QApplication([])
    unittest.main()
