from PyQt6.QtWidgets import (
    QPushButton, QLabel, QLineEdit, QVBoxLayout, QHBoxLayout, QTableWidget, QTableWidgetItem,
    QWidget, QMessageBox, QGroupBox, QStackedWidget, QInputDialog, QDoubleSpinBox
)
from PyQt6.QtCore import QSize, Qt
from PyQt6.QtGui import QScreen
from database.database import (fetch_movies, fetch_movies_by_title,
                               fetch_films_by_ids, get_film_id_by_name, add_or_update_user_rating, fetch_user_reviews)
from model.functions import recommend_movies_with_model


class SearchRecommendationWindow(QWidget):
    def __init__(self, on_logout_callback, user_id):
        super().__init__()
        self.on_logout_callback = on_logout_callback
        self.user_id = user_id
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

    def center_window(self):
        screen = self.screen()
        screen_geometry = screen.geometry()
        window_geometry = self.frameGeometry()
        window_geometry.moveCenter(screen_geometry.center())
        self.move(window_geometry.topLeft())

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

        self.make_review = QPushButton("Review")
        self.make_review.clicked.connect(self.show_review_ui)

        self.log_out_button = QPushButton("Log Out")
        self.log_out_button.clicked.connect(self.log_out)

        self.button_layout.addWidget(self.search_button)
        self.button_layout.addWidget(self.recommend_button)
        self.button_layout.addWidget(self.top_movies_button)
        self.button_layout.addWidget(self.make_review)
        self.button_layout.addWidget(self.log_out_button)

        # Stacked widget to switch between the different UIs
        self.stacked_widget = QStackedWidget()
        self.stacked_widget.setFixedHeight(160)  # Set a fixed height for all UIs

        # Create Search UI
        self.search_ui = self.create_search_ui()
        self.stacked_widget.addWidget(self.search_ui)

        # Create Recommendation UI
        self.recommend_ui = self.create_recommend_ui()
        self.stacked_widget.addWidget(self.recommend_ui)

        # Create Top Movies UI
        self.top_movies_ui = self.create_top_movies_ui()
        self.stacked_widget.addWidget(self.top_movies_ui)

        # Create Review UI
        self.review_ui = self.create_review_ui()
        self.stacked_widget.addWidget(self.review_ui)

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
        self.center_window()

    def create_review_ui(self):
        """Create the UI for reviewing a movie."""
        review_group = QGroupBox("Review a Movie")
        review_layout = QVBoxLayout()

        self.review_label = QLabel("Enter movie title:")
        self.review_input = QLineEdit()
        self.review_input.setPlaceholderText("Enter movie title...")

        self.rating_label = QLabel("Enter your rating (1.0 - 10.0):")
        self.rating_input = QDoubleSpinBox()
        self.rating_input.setRange(1.0, 10.0)
        self.rating_input.setSingleStep(0.1)
        self.rating_input.setValue(5.0)

        self.submit_review_button = QPushButton("Review a Film")
        self.submit_review_button.clicked.connect(self.submit_review)

        self.reviews_label = QLabel("Your Reviews:")
        self.reviews_table = QTableWidget()
        self.reviews_table.setColumnCount(2)
        self.reviews_table.setHorizontalHeaderLabels(['Movie ID', 'Rating'])

        review_layout.addWidget(self.review_label)
        review_layout.addWidget(self.review_input)
        review_layout.addWidget(self.rating_label)
        review_layout.addWidget(self.rating_input)
        review_layout.addWidget(self.submit_review_button)
        review_layout.addWidget(self.reviews_label)
        review_layout.addWidget(self.reviews_table)

        review_group.setLayout(review_layout)
        review_group.setFixedHeight(400)
        return review_group

    def show_review_ui(self):
        """Switch to the Review UI."""
        self.stacked_widget.setCurrentWidget(self.review_ui)
        self.load_user_reviews()

    def load_user_reviews(self):
        """Load and display reviews for the logged-in user."""
        reviews = fetch_user_reviews(self.user_id)
        self.reviews_table.setRowCount(0)
        for row_data in reviews:
            row_idx = self.reviews_table.rowCount()
            self.reviews_table.insertRow(row_idx)
            for col_idx, value in enumerate(row_data):
                if col_idx >= 2:
                    item = QTableWidgetItem(str(value))
                    self.reviews_table.setItem(row_idx, col_idx - 2, item)
        self.reviews_table.resizeColumnsToContents()

    def submit_review(self):
        """Submit the user's review to the database."""
        movie_title = self.review_input.text()
        rating = self.rating_input.value()
        if not movie_title:
            QMessageBox.warning(self, "Error", "Please enter a movie title.")
            return
        # Get the movie ID from the movie title
        movie_id = get_film_id_by_name(movie_title)
        if not movie_id:
            QMessageBox.warning(self, "Error", "Movie not found.")
            return
        # Submit the review to the database
        status = add_or_update_user_rating(self.user_id, movie_id, rating)
        QMessageBox.information(self, "Review Status", status)
        # Reload user reviews to show the new review
        self.load_user_reviews()

    def log_out(self):
        """Handle user log out."""
        # Show confirmation dialog before logging out
        reply = QMessageBox.question(
            self, 'Log Out', 'Are you sure you want to log out?',
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,
            QMessageBox.StandardButton.No
        )

        if reply == QMessageBox.StandardButton.Yes:
            QMessageBox.information(self, "Logged Out", "You have successfully logged out.")
            self.on_logout_callback()

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
        top_movies_label = QLabel("Top 10 Movies by Ratings")
        top_movies_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        top_movies_layout.addWidget(top_movies_label)

        # Create the "Show More" button for Top Movies UI
        self.show_more_button = QPushButton("Show More")
        self.show_more_button.clicked.connect(lambda: self.show_more(top_movies_label))
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
        """Fetch movie recommendations based on the input title or ID."""
        film_name_or_id = self.recommend_input.text()
        if not film_name_or_id:
            QMessageBox.warning(self, "Error", "Please enter a movie name or ID.")
            return
        film_id = None
        try:
            film_id = int(film_name_or_id)
        except ValueError:
            film_id = get_film_id_by_name(film_name_or_id)
        # Get recommendations using the model
        recommendation = recommend_movies_with_model(film_id).tolist()
        # Debugging output to check the recommendation
        # Check if the recommendation is a valid list of movie IDs
        # Fetch movies by the list of recommended IDs
        movies = fetch_films_by_ids(recommendation)
        # Check if we received valid movie data
        if not movies:
            QMessageBox.information(self, "No Recommendations", "No movies found for the given recommendations.")
            return

        # Display the recommended movies
        self.show_recommendations(movies)
        # Optionally, inform the user that recommendations have been displayed
        QMessageBox.information(self, "Recommendation", "Recommended Films based on your query.")

    def show_more(self, top_movies_label):
        """Show more movies when the user clicks 'Show More'."""
        movies = fetch_movies(offset=self.offset, limit=self.limit)
        if not movies:
            self.show_more_button.setEnabled(False)
            QMessageBox.information(self, "No More Movies", "No more movies available.")
            return
        self.display_results(movies)
        current_count = self.offset
        top_movies_label.setText(f"Top {current_count} Movies by Ratings")

    def show_top_recommendations(self):
        """Fetch and display the top 10 most popular movies."""
        movies = fetch_movies(offset=self.offset, limit=10)
        if movies:
            self.tableWidget.setRowCount(0)
            self.display_results(movies)
        else:
            QMessageBox.information(self, "No More Movies", "No more movies available.")

    def show_recommendations(self, movies):
        """Fetch and display recommended movies."""
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