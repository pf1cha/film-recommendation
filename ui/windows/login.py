from PyQt6.QtWidgets import (
    QPushButton, QLabel, QLineEdit, QVBoxLayout,
    QWidget, QMessageBox
)
from database.database import authenticate_user

class LoginWindow(QWidget):
    def __init__(self, on_complete_callback, callback_button):
        super().__init__()
        self.on_complete_callback = on_complete_callback
        self.callback_button = callback_button
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
        result = authenticate_user(username, password)
        if result == "Authentication successful.":
            QMessageBox.information(self, "Login Successful", "You are now logged in!")
            self.on_complete_callback()
            self.close()
        else:
            QMessageBox.warning(self, "Authentication Failed", result)

    def back_to_main(self):
        self.callback_button()
        self.close()
