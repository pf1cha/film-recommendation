import sys
from PyQt6.QtWidgets import QMainWindow, QPushButton, QVBoxLayout, QStackedLayout, QWidget, QApplication
from ui.windows.registration import RegistrationWindow
from ui.windows.login import LoginWindow
from ui.windows.search import SearchRecommendationWindow

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Welcome")
        self.setGeometry(100, 100, 300, 200)
        self.setStyleSheet("""
            QPushButton {
                background-color: #4CAF50;
                color: white;
                border-radius: 5px;
                padding: 10px;
            }
            QPushButton:hover {
                background-color: #45a049;
            }
            QLabel {
                font-size: 14px;
            }
        """)
        self.init_ui()
        self.username = None
        self.user_id = None

    def init_ui(self):
        # Create QStackedLayout for switching between views
        self.layout = QStackedLayout()
        self.container = QWidget()
        self.container.setLayout(self.layout)
        self.setCentralWidget(self.container)

        # Initialize and add the first view (Welcome screen with Register/Login options)
        self.main_page = QWidget()
        self.main_layout = QVBoxLayout(self.main_page)

        # Add Register and Log In buttons
        self.register_button = QPushButton("Register")
        self.register_button.clicked.connect(self.open_registration)
        self.login_button = QPushButton("Log In")
        self.login_button.clicked.connect(self.open_login)

        # Add buttons to the layout of the welcome page
        self.main_layout.addWidget(self.register_button)
        self.main_layout.addWidget(self.login_button)

        # Add the welcome page to the stacked layout
        self.layout.addWidget(self.main_page)


    def open_registration(self):
        """Handle the Registration Window"""
        self.registration_window = RegistrationWindow(self.on_registration_complete)
        self.layout.addWidget(self.registration_window)
        self.layout.setCurrentWidget(self.registration_window)

    def on_registration_complete(self):
        """Switch back to the main welcome page after successful registration"""
        self.layout.setCurrentWidget(self.main_page)

    def on_login_complete(self, username, user_id):
        """Handle the successful login and switch to the main content view"""
        self.username = username
        self.user_id = user_id
        self.show_search_recommendation_view()

    def open_login(self):
        """Handle the Login Window"""
        self.login_window = LoginWindow(self.on_login_complete, self.on_registration_complete)
        self.layout.addWidget(self.login_window)
        self.layout.setCurrentWidget(self.login_window)

    def show_search_recommendation_view(self):
        """Show the search and recommendation view after login"""
        # Create an instance of SearchRecommendationWindow (your existing search and recommendation window)
        self.search_recommendation_window = SearchRecommendationWindow(self.on_logout, user_id=self.user_id)
        # Add it to the stacked layout
        self.layout.addWidget(self.search_recommendation_window)
        # Switch to the search/recommendation view
        self.layout.setCurrentWidget(self.search_recommendation_window)
        self.setWindowTitle(f"Welcome, {self.username}")
        self.resize(1000, 500)

    def on_logout(self):
        """Handle the logout and show the welcome screen"""
        self.username = None
        self.user_id = None
        self.layout.setCurrentWidget(self.main_page)
        self.setWindowTitle("Welcome")
        self.resize(100, 100)
