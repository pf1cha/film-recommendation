from PyQt6.QtWidgets import (
    QPushButton, QLabel, QLineEdit, QVBoxLayout, QHBoxLayout, QTableWidget, QTableWidgetItem,
    QWidget, QMessageBox, QGroupBox, QStackedWidget
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

        # Button layout for the top buttons (Search, Recommendation, Top Movies by Ratings)
        self.button_layout = QHBoxLayout()
        self.search_button = QPushButton("Search")
        self.search_button.clicked.connect(self.show_search_ui)

        self.recommend_button = QPushButton("Recommendation")
        self.recommend_button.clicked.connect(self.show_recommend_ui)

        self.top_movies_button = QPushButton("Top Movies By Ratings")
        self.top_movies_button.clicked.connect(self.show_top_movies_ui)

        self.button_layout.addWidget(self.search_button)
        self.button_layout.addWidget(self.recommend_button)
        self.button_layout.addWidget(self.top_movies_button)

        # Stacked widget to switch between the different UIs
        self.stacked_widget = QStackedWidget()
        self.stacked_widget.setFixedHeight(400)  # Set a fixed height for all UIs

        # Create Search UI
        self.search_ui = self.create_search_ui()
        self.stacked_widget.addWidget(self.search_ui)

        # Create Recommendation UI
        self.recommend_ui = self.create_recommend_ui()
        self.stacked_widget.addWidget(self.recommend_ui)

        # Create Top Movies UI
        self.top_movies_ui = self.create_top_movies_ui()
        self.stacked_widget.addWidget(self.top_movies_ui)

        # Layout to hold button layout and stacked widget
        layout.addLayout(self.button_layout)
        layout.addWidget(self.stacked_widget)

        # Add the table for all views
        self.tableWidget = QTableWidget()
        self.tableWidget.setColumnCount(10)
        self.tableWidget.setHorizontalHeaderLabels([
            'ID', 'Title', 'Release Date', 'Genre', 'Revenue', 'Budget', 'Rating', 'Votes', 'Profit', 'Language'
        ])
        layout.addWidget(self.tableWidget)
        self.setLayout(layout)

    def create_search_ui(self):
        search_group = QGroupBox("Search Movies")
        search_layout = QVBoxLayout()

        self.search_label = QLabel("Enter movie title:")
        self.search_input = QLineEdit()
        self.search_input.setPlaceholderText("Search for a movie...")

        self.search_action_button = QPushButton("Search")
        self.search_action_button.clicked.connect(self.search_film)

        search_layout.addWidget(self.search_label)
        search_layout.addWidget(self.search_input)
        search_layout.addWidget(self.search_action_button)

        search_group.setLayout(search_layout)
        return search_group

    def create_recommend_ui(self):
        recommend_group = QGroupBox("Movie Recommendations")
        recommend_layout = QVBoxLayout()

        self.recommend_input_label = QLabel("Enter Movie Name or ID:")
        self.recommend_input = QLineEdit()
        self.recommend_input.setPlaceholderText("Enter a movie title or ID...")

        self.recommend_action_button = QPushButton("Recommend")
        self.recommend_action_button.clicked.connect(self.get_recommendation)

        recommend_layout.addWidget(self.recommend_input_label)
        recommend_layout.addWidget(self.recommend_input)
        recommend_layout.addWidget(self.recommend_action_button)

        recommend_group.setLayout(recommend_layout)
        return recommend_group

    def create_top_movies_ui(self):
        # Create the group box for Top Movies
        top_movies_group = QGroupBox("Top Movies By Ratings")
        # Set margins for better alignment
        top_movies_group.setContentsMargins(5, 5, 5, 5)  # left, top, right, bottom

        top_movies_layout = QVBoxLayout()
        top_movies_layout.addWidget(QLabel("Top 10 Movies by Ratings"))

        # Create the "Show More" button for Top Movies UI
        self.show_more_button = QPushButton("Show More")
        self.show_more_button.clicked.connect(self.show_more)
        top_movies_layout.addWidget(self.show_more_button)

        # Set the layout for the Top Movies Group Box
        top_movies_group.setLayout(top_movies_layout)

        return top_movies_group

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

        self.tableWidget.setRowCount(0)
        self.offset = 0

        results = fetch_movies_by_title(film_name)
        if results:
            self.display_results(results)
        else:
            QMessageBox.information(self, "No Results", "No films found matching your search.")

    def get_recommendation(self):
        """Fetch movie recommendations."""
        film_name_or_id = self.recommend_input.text()
        if not film_name_or_id:
            QMessageBox.warning(self, "Error", "Please enter a movie name or ID.")
            return

        # Placeholder for your recommendation logic
        QMessageBox.information(self, "Recommendation", "Recommended Films based on your query.")
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
        movies = fetch_movies(offset=self.offset, limit=10)
        if movies:
            self.tableWidget.setRowCount(0)
            self.display_results(movies)
        else:
            QMessageBox.information(self, "No More Movies", "No more movies available.")

    def show_recommendations(self):
        """Fetch and display recommended movies."""
        movies = fetch_movies(offset=self.offset, limit=self.limit)
        if movies:
            self.tableWidget.setRowCount(0)
            self.display_results(movies)
        else:
            QMessageBox.information(self, "No Recommendations", "No recommendations found.")

    def show_search_ui(self):
        self.tableWidget.setRowCount(0)  # Clear table when switching to Search
        self.stacked_widget.setCurrentWidget(self.search_ui)

    def show_recommend_ui(self):
        self.tableWidget.setRowCount(0)  # Clear table when switching to Recommendation
        self.stacked_widget.setCurrentWidget(self.recommend_ui)

    def show_top_movies_ui(self):
        self.tableWidget.setRowCount(0)  # Clear table when switching to Top Movies
        self.offset = 0  # Reset the offset
        self.stacked_widget.setCurrentWidget(self.top_movies_ui)
        self.show_top_recommendations()