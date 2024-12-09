from PyQt6.QtWidgets import (
    QPushButton, QLabel, QLineEdit, QVBoxLayout,
    QWidget, QMessageBox
)
from database.database import add_user
from utils.utils import hash_password

class RegistrationWindow(QWidget):
    def __init__(self, on_complete_callback):
        super().__init__()
        self.on_complete_callback = on_complete_callback
        self.setWindowTitle("Register")
        self.setGeometry(350, 350, 300, 200)
        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout()

        self.username_label = QLabel("Username:")
        self.username_input = QLineEdit()

        self.password_label = QLabel("Password:")
        self.password_input = QLineEdit()
        self.password_input.setEchoMode(QLineEdit.EchoMode.Password)

        self.register_button = QPushButton("Register")
        self.register_button.clicked.connect(self.register_user)

        self.back_button = QPushButton("Back")
        self.back_button.clicked.connect(self.back_to_main)

        layout.addWidget(self.username_label)
        layout.addWidget(self.username_input)
        layout.addWidget(self.password_label)
        layout.addWidget(self.password_input)
        layout.addWidget(self.register_button)
        layout.addWidget(self.back_button)

        self.setLayout(layout)

    def register_user(self):
        username = self.username_input.text()
        password = self.password_input.text()

        if not username or not password:
            QMessageBox.warning(self, "Error", "Please fill out all fields.")
            return

        hashed_password = hash_password(password)

        result_message = add_user(username, hashed_password)

        if "successfully" in result_message:
            QMessageBox.information(self, "Success", result_message)
            self.on_complete_callback()  # Callback to switch back to the main window
            self.close()  # Close the registration window
        else:
            QMessageBox.warning(self, "Error", result_message)

    def back_to_main(self):
        # Go back to the main window (Welcome screen)
        self.on_complete_callback()
        self.close()
