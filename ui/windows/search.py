from PyQt6.QtWidgets import (
    QPushButton, QLabel, QLineEdit, QVBoxLayout, QTableWidget, QTableWidgetItem,
    QWidget, QMessageBox
)
from sqlalchemy import create_engine, select, desc
from sqlalchemy.orm import sessionmaker
from database.database_info import content_table
from database.db_password import DATABASE_URL
from database.database import fetch_movies, fetch_movies_by_title


class SearchRecommendationWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Search and Recommendation")
        self.setGeometry(100, 100, 1000, 400)
        # Pagination variables
        self.offset = 0
        self.limit = 10
        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout()

        self.search_label = QLabel("Search for a film:")
        self.search_input = QLineEdit()

        self.search_button = QPushButton("Search")
        self.search_button.clicked.connect(self.search_film)

        self.recommend_button = QPushButton("Get Recommendation")
        self.recommend_button.clicked.connect(self.get_recommendation)

        # Table setup
        self.tableWidget = QTableWidget()
        # Setting up the table with headers
        # self.tableWidget.setRowCount(10)  # Set row count based on the number of entries
        self.tableWidget.setColumnCount(10)  # Number of columns in the data

        # Set the column headers
        self.tableWidget.setHorizontalHeaderLabels([
            'ID', 'Title', 'Release Date', 'Genre', 'Revenue', 'Budget', 'Rating', 'Votes', 'Profit', 'Language'
        ])

        self.show_more_button = QPushButton("Show More")
        self.show_more_button.clicked.connect(self.show_more)

        layout.addWidget(self.search_label)
        layout.addWidget(self.search_input)
        layout.addWidget(self.search_button)
        layout.addWidget(self.recommend_button)
        layout.addWidget(self.tableWidget)
        layout.addWidget(self.show_more_button)

        self.setLayout(layout)

        # Load initial data
        self.load_movies()

    def load_movies(self):
        """Load movies from the database and display them in the table."""
        movies = fetch_movies(offset=self.offset, limit=self.limit)
        self.display_results(movies)
        # Increment the offset for pagination

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

        # Fetch matching movies using the standalone function
        results = fetch_movies_by_title(film_name)
        if results:
            self.display_results(results)
        else:
            QMessageBox.information(self, "No Results", "No films found matching your search.")

    def get_recommendation(self):
        QMessageBox.information(self, "Recommendation", "Recommended Film: Inception")

    def show_more(self):
        movies = fetch_movies(offset=self.offset, limit=self.limit)
        # If there are no more movies, show a message
        if not movies:
            QMessageBox.information(self, "No More Movies", "No more movies available.")
            return
        self.display_results(movies)

