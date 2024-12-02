from PyQt6.QtWidgets import (
    QPushButton, QLabel, QLineEdit, QVBoxLayout,
    QWidget, QMessageBox
)
from database.database import add_user
import hashlib


def hash_password(password):
    """Hash the password using SHA-256."""
    return hashlib.sha256(password.encode()).hexdigest()


class RegistrationWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Register")
        self.setGeometry(350, 350, 300, 200)

        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout()
        self.username_label = QLabel("Username:")
        self.username_input = QLineEdit()

        self.password_label = QLabel("Password:")
        self.password_input = QLineEdit()
        # self.password_input.setEchoMode(QLineEdit.Password)

        self.register_button = QPushButton("Register")
        self.register_button.clicked.connect(self.register_user)

        layout.addWidget(self.username_label)
        layout.addWidget(self.username_input)
        layout.addWidget(self.password_label)
        layout.addWidget(self.password_input)
        layout.addWidget(self.register_button)

        self.setLayout(layout)

    def register_user(self):
        username = self.username_input.text()
        password = self.password_input.text()

        if not username or not password:
            QMessageBox.warning(self, "Error", "Please fill out all fields.")
            return

        hashed_password = hash_password(password)
        print(username, hashed_password)
        result_message = add_user(username, hashed_password)

        if "successfully" in result_message:
            QMessageBox.information(self, "Success", result_message)
            self.close()
        else:
            QMessageBox.warning(self, "Error", result_message)