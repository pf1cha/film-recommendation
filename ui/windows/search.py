from PyQt6.QtWidgets import (
    QPushButton, QLabel, QLineEdit, QVBoxLayout,
    QWidget, QMessageBox
)

class SearchRecommendationWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Search and Recommendation")
        self.setGeometry(350, 350, 400, 200)

        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout()

        self.search_label = QLabel("Search for a film:")
        self.search_input = QLineEdit()

        self.search_button = QPushButton("Search")
        self.search_button.clicked.connect(self.search_film)

        self.recommend_button = QPushButton("Get Recommendation")
        self.recommend_button.clicked.connect(self.get_recommendation)

        layout.addWidget(self.search_label)
        layout.addWidget(self.search_input)
        layout.addWidget(self.search_button)
        layout.addWidget(self.recommend_button)

        self.setLayout(layout)

    def search_film(self):
        film_name = self.search_input.text()
        if film_name:
            QMessageBox.information(self, "Search Result", f"Results for '{film_name}'")
        else:
            QMessageBox.warning(self, "Error", "Please enter a film name.")

    def get_recommendation(self):
        QMessageBox.information(self, "Recommendation", "Recommended Film: Inception")
