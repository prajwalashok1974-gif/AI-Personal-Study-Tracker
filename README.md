# AI-Powered Personal Study Tracker

A local Streamlit application that combines study-session logging, SQLite persistence, interactive analytics, PDF reporting, and a scikit-learn Random Forest model for productivity estimation.

## Features

- User registration and login
- Study-session tracking with subject, technique, mood, distractions, caffeine, and productivity
- Per-user session history stored in SQLite
- Productivity and study-duration analytics with Plotly
- Interactive dashboard filters and visual summaries
- Productivity prediction from session features
- Downloadable PDF study reports
- Reproducible sample-data generation, ingestion, and model-training scripts

## Technology

Python · Streamlit · SQLite · pandas · Plotly · scikit-learn · SQLAlchemy · joblib · FPDF

## Project structure

```text
frontend/streamlit_app.py       # Streamlit UI and dashboard
backend/src/generate_sample.py  # Generate sample sessions
backend/src/ingest.py           # Load CSV data into SQLite
backend/src/train_model.py      # Train and save the Random Forest pipeline
backend/src/utils.py            # Database, authentication, and session helpers
backend/models/pipeline.joblib  # Saved model pipeline
database/sql/schema.sql         # SQLite schema
database/data/                 # Local sample data and database
```

## Setup

```bash
git clone https://github.com/prajwalashok1974-gif/AI-Personal-Study-Tracker.git
cd AI-Personal-Study-Tracker
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
streamlit run frontend/streamlit_app.py
```

The app initializes the SQLite schema on startup. Register a local account, sign in, and add study sessions from the dashboard.

## Data and model workflow

```bash
python backend/src/generate_sample.py
python backend/src/ingest.py
python backend/src/train_model.py
```

The model uses session duration, subject, technique, distractions, mood, and caffeine intake to estimate the self-rated productivity score. Categorical fields are one-hot encoded and the trained pipeline is saved with joblib.

## Analytics and reports

The dashboard includes session totals, productivity summaries, subject and technique analysis, mood/distraction comparisons, and time-based trends. Users can generate a PDF report containing totals and recent sessions.

## Security note

This is a local learning project. It stores local account data in SQLite; do not use real passwords or deploy it with sensitive data without replacing the authentication and security design with production-grade controls.