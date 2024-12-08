import sys
from PyQt6.QtWidgets import (
    QApplication, QMainWindow,
    QPushButton, QVBoxLayout,
    QWidget
)
from ui.windows.registration import RegistrationWindow
from ui.windows.login import LoginWindow

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Welcome")
        self.setGeometry(500, 500, 300, 200)
        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout()

        self.register_button = QPushButton("Register")
        self.register_button.clicked.connect(self.open_registration)

        self.login_button = QPushButton("Log In")
        self.login_button.clicked.connect(self.open_login)

        layout.addWidget(self.register_button)
        layout.addWidget(self.login_button)

        container = QWidget()
        container.setLayout(layout)
        self.setCentralWidget(container)

    def open_registration(self):
        self.registration_window = RegistrationWindow()
        self.registration_window.show()

    def open_login(self):
        self.login_window = LoginWindow()
        self.login_window.show()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    main_window = MainWindow()
    main_window.show()
    sys.exit(app.exec())
