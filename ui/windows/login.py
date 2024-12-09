from PyQt6.QtWidgets import (
    QPushButton, QLabel, QLineEdit, QVBoxLayout,
    QWidget, QMessageBox
)
from database.database import authenticate_user

class LoginWindow(QWidget):
    def __init__(self, login_callback, registration_callback):
        super().__init__()
        self.login_callback = login_callback
        self.registration_callback = registration_callback
        self.setWindowTitle("Log In")
        self.setGeometry(350, 350, 300, 200)
        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout()

        self.username_label = QLabel("Username:")
        self.username_input = QLineEdit()

        self.password_label = QLabel("Password:")
        self.password_input = QLineEdit()
        # self.password_input.setEchoMode(QLineEdit.Password)

        self.login_button = QPushButton("Log In")
        self.login_button.clicked.connect(self.login_user)

        self.back_button = QPushButton("Back")
        self.back_button.clicked.connect(self.back_to_main)

        layout.addWidget(self.username_label)
        layout.addWidget(self.username_input)
        layout.addWidget(self.password_label)
        layout.addWidget(self.password_input)
        layout.addWidget(self.login_button)
        layout.addWidget(self.back_button)

        self.setLayout(layout)

    def login_user(self):
        username = self.username_input.text()
        password = self.password_input.text()
        if not username or not password:
            QMessageBox.warning(self, "Input Error", "Please enter both username and password.")
            return
        status, user_id = authenticate_user(username, password)
        if status == "Authentication successful.":
            self.login_callback(username, user_id)
            QMessageBox.information(self, "Login Successful", "You are now logged in!")
            self.close()
        else:
            QMessageBox.warning(self, "Authentication Failed", status)

    def back_to_main(self):
        self.registration_callback()
        self.close()
