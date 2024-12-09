from PyQt6.QtWidgets import (
    QPushButton, QLabel, QLineEdit, QVBoxLayout, QTableWidget, QTableWidgetItem,
    QWidget, QMessageBox
)
from database.database import fetch_movies, fetch_movies_by_title


class SearchRecommendationWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Search and Recommendation")
        self.setGeometry(100, 100, 1000, 500)  # Adjust window size
        # Pagination variables
        self.offset = 0
        self.limit = 10
        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout()

        # Search section components
        self.search_label = QLabel("Search for a film:")
        self.search_input = QLineEdit()

        self.search_button = QPushButton("Search")
        self.search_button.clicked.connect(self.search_film)

        # Recommendation section components
        self.recommend_button = QPushButton("Get Recommendation")
        self.recommend_button.clicked.connect(self.get_recommendation)

        # Top movies section
        self.top_recommend_button = QPushButton("Top 10 Popular Movies")
        self.top_recommend_button.clicked.connect(self.show_top_recommendations)

        # Table setup
        self.tableWidget = QTableWidget()
        self.tableWidget.setColumnCount(10)  # Number of columns in the data
        self.tableWidget.setHorizontalHeaderLabels([
            'ID', 'Title', 'Release Date', 'Genre', 'Revenue', 'Budget', 'Rating', 'Votes', 'Profit', 'Language'
        ])

        self.show_more_button = QPushButton("Show More")
        self.show_more_button.clicked.connect(self.show_more)

        # Add all widgets to the layout
        layout.addWidget(self.search_label)
        layout.addWidget(self.search_input)
        layout.addWidget(self.search_button)
        layout.addWidget(self.recommend_button)
        layout.addWidget(self.top_recommend_button)  # Added button for Top Movies
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

