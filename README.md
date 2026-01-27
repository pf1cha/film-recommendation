# Film Recommendation

A desktop movie recommendation application built with Python and PyQt6. 
The project combines data processing, a local database, 
and model-based recommenders to provide film suggestions.

## Key features
- Desktop GUI built with `PyQt6` (`ui/windows`).
- Data ingestion and cleaning utilities in `data/` and `data_clearing/`.
- Local database management and utilities in `database/`.
- Recommender models and training in `model/` and `user_recom/`.
- Unit tests under `tests/`.

## Requirements
- Python 3.10+
- `pip` and a virtual environment tool
- See `requirements.txt` for exact dependencies (includes `PyQt6`, numerical and ML libraries).


## Running the application
- From the project root run:
  - `python main.py`
- The main GUI entrypoint is `main.py` which creates the `QApplication` and shows `ui/windows/user_interface.MainWindow`.

## Project structure (high level)
- `main.py` - application entrypoint.
- `ui/windows/` - PyQt6 windows: `login.py`, `registration.py`, `search.py`, `user_interface.py`.
- `data/` - CSV datasets used by the project.
- `data_clearing/` - data cleaning and transformation helpers.
- `database/` - DB helpers, local creation scripts and credentials helper (`db_password.py`).
- `model/` - data preparation, model building and test utilities plus pretrained artifacts.
- `user_recom/` - user-focused recommender build scripts.
- `utils/` - shared utility functions.

## Database
- Database helper scripts are in `database/`.
- If using a local DB, review `database/local_database_creation.py` and `database/db_password.py` before running.

## Development notes
- Model training and experiments are under `model/`. Pretrained artifacts may be present (for example `movie2movie_recommender.pth`).
- Data files are located in `data/`; large or private datasets are not included.
- Use `venv\Scripts\activate` on Windows before running scripts.

## Additional information about the project
The data was collected from 3 different datasets from kaggle, then cleaned and merged to create a comprehensive movie database.

## Plans for improvements
- Improve GUI design and user experience.
- Add more recommendation algorithms.