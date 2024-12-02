from PyQt6.QtWidgets import (
    QPushButton, QLabel, QLineEdit, QVBoxLayout,
    QWidget, QMessageBox
)
from ui.windows.search import SearchRecommendationWindow

class LoginWindow(QWidget):
    def __init__(self):
        super().__init__()
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

        layout.addWidget(self.username_label)
        layout.addWidget(self.username_input)
        layout.addWidget(self.password_label)
        layout.addWidget(self.password_input)
        layout.addWidget(self.login_button)

        self.setLayout(layout)

    def login_user(self):
        username = self.username_input.text()
        password = self.password_input.text()

        # Placeholder for authentication logic
        if username and password:
            QMessageBox.information(self, "Success", "Log in successful!")
            self.open_search_recommendation()
            self.close()
        else:
            QMessageBox.warning(self, "Error", "Invalid credentials.")

    def open_search_recommendation(self):
        self.search_window = SearchRecommendationWindow()
        self.search_window.show()
