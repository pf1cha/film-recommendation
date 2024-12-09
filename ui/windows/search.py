from PyQt6.QtWidgets import (
    QPushButton, QLabel, QLineEdit, QVBoxLayout, QHBoxLayout, QTableWidget, QTableWidgetItem,
    QWidget, QMessageBox, QGroupBox, QFrame
)
from PyQt6.QtCore import QSize, Qt
from PyQt6.QtGui import QColor, QPalette
from database.database import fetch_movies, fetch_movies_by_title


class SearchRecommendationWindow(QWidget):
    def __init__(self):
        super().__init__()
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
            QLineEdit {
                padding: 10px;
                border-radius: 5px;
                border: 1px solid #ccc;
            }
            QTableWidget {
                border: 1px solid #ccc;
                gridline-color: #e0e0e0;
                background-color: #f9f9f9;
                color: black;  # Set text color to black
            }
            QTableWidget::item {
                padding: 8px;
            }
            QTableWidget::item:hover {
                background-color: #f0f0f0;
            }
            QLabel {
                font-size: 14px;
            }
        """)
        self.offset = 0
        self.limit = 10
        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout()

        # Search section
        search_group = QGroupBox("Search Movies")
        search_layout = QVBoxLayout()
        self.search_label = QLabel("Enter movie title:")
        self.search_input = QLineEdit()
        self.search_input.setPlaceholderText("Search for a movie...")

        self.search_button = QPushButton("Search")
        self.search_button.clicked.connect(self.search_film)

        # Layout for search section
        search_layout.addWidget(self.search_label)
        search_layout.addWidget(self.search_input)
        search_layout.addWidget(self.search_button)
        search_group.setLayout(search_layout)

        # Recommendation section
        recommend_group = QGroupBox("Movie Recommendations")
        recommend_layout = QVBoxLayout()
        self.recommend_button = QPushButton("Get Recommendation")
        self.recommend_button.clicked.connect(self.get_recommendation)

        self.top_recommend_button = QPushButton("Top 10 Popular Movies")
        self.top_recommend_button.clicked.connect(self.show_top_recommendations)

        # Layout for recommendations section
        recommend_layout.addWidget(self.recommend_button)
        recommend_layout.addWidget(self.top_recommend_button)
        recommend_group.setLayout(recommend_layout)

        # Table setup
        self.tableWidget = QTableWidget()
        self.tableWidget.setColumnCount(10)  # Number of columns in the data
        self.tableWidget.setHorizontalHeaderLabels([
            'ID', 'Title', 'Release Date', 'Genre', 'Revenue', 'Budget', 'Rating', 'Votes', 'Profit', 'Language'
        ])
        # self.tableWidget.setEditTriggers(QTableWidget.EditTriggers.NoEditTriggers)  # Disable editing in table
        # self.tableWidget.setSelectionMode(QTableWidget.SelectionMode.SingleSelection)  # Single row selection

        self.show_more_button = QPushButton("Show More")
        self.show_more_button.clicked.connect(self.show_more)
        self.show_more_button.setEnabled(True)

        # Add widgets to layout
        layout.addWidget(search_group)
        layout.addWidget(recommend_group)
        layout.addWidget(self.tableWidget)
        layout.addWidget(self.show_more_button)

        self.setLayout(layout)

        # Load initial data (e.g., fetch top movies)
        self.load_movies()

    def load_movies(self):
        """Load movies from the database and display them in the table."""
        movies = fetch_movies(offset=self.offset, limit=self.limit)
        self.display_results(movies)

    def display_results(self, movies):
        """Display a list of movies in the table widget."""
        self.offset += self.limit
        current_row_count = self.tableWidget.rowCount()
        for row_data in movies:
            row_idx = current_row_count
            self.tableWidget.insertRow(row_idx)
            for col_idx, value in enumerate(row_data):
                item = QTableWidgetItem(str(value))
                self.tableWidget.setItem(row_idx, col_idx, item)
        self.tableWidget.resizeColumnsToContents()

    def search_film(self):
        """Search for films by title and display all matching results."""
        film_name = self.search_input.text()
        if not film_name:
            QMessageBox.warning(self, "Error", "Please enter a film name.")
            return

        # Reset the table for the new search
        self.tableWidget.setRowCount(0)
        self.offset = 0

        results = fetch_movies_by_title(film_name)
        if results:
            self.display_results(results)
        else:
            QMessageBox.information(self, "No Results", "No films found matching your search.")

    def get_recommendation(self):
        """Display a generic recommendation (replace with your logic)."""
        # Placeholder: this would be replaced with an actual recommendation logic
        QMessageBox.information(self, "Recommendation", "Recommended Film: Inception")
        # You can replace this with a call to your database to fetch personalized recommendations.
        self.show_recommendations()

    def show_more(self):
        """Show more movies when the user clicks 'Show More'."""
        movies = fetch_movies(offset=self.offset, limit=self.limit)
        if not movies:
            self.show_more_button.setEnabled(False)
            QMessageBox.information(self, "No More Movies", "No more movies available.")
            return
        self.display_results(movies)

    def show_top_recommendations(self):
        """Fetch and display the top 10 most popular movies."""
        movies = fetch_movies(offset=self.offset, limit=10)  # Fetch the top 10 movies
        if movies:
            self.tableWidget.setRowCount(0)  # Clear the table before loading new data
            self.display_results(movies)
        else:
            QMessageBox.information(self, "No More Movies", "No more movies available.")

    def show_recommendations(self):
        """Fetch and display recommended movies (this can be replaced with a real recommendation engine)."""
        # Placeholder: Replace this with your actual recommendation fetching logic
        movies = fetch_movies(offset=self.offset, limit=self.limit)
        if movies:
            self.tableWidget.setRowCount(0)  # Clear the table before loading new data
            self.display_results(movies)
        else:
            QMessageBox.information(self, "No Recommendations", "No recommendations found.")
