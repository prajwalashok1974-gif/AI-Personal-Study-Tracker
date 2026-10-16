## AI-Powered Personal Study Tracker

An intelligent productivity analytics app built with **Python**, **SQLite**, **Machine Learning**, and **Streamlit**.  
It empowers learners to track, visualize, and improve their study habits while using AI to estimate their expected productivity.
  
---

## Overview

The **AI-Powered Personal Study Tracker** transforms daily study logs into actionable insights.  
It leverages a **Random Forest Regressor** to model productivity based on mood, distractions, study duration, caffeine intake, and more.

You can:
- Log study sessions (with mood, focus level, and caffeine)
- Analyze study performance trends and patterns
- Estimate expected productivity before studying
- View aggregated insights and KPIs

---

## Project Structure

```
ai-study-tracker/
├── frontend/
│   └── streamlit_app.py         # Streamlit dashboard and UI
├── backend/
│   ├── models/
│   │   └── pipeline.joblib      # Saved ML model
│   └── src/
│       ├── generate_sample.py   # Generate synthetic study sessions
│       ├── ingest.py            # Load CSV into SQLite
│       ├── train_model.py       # Train RandomForestRegressor
│       └── utils.py             # Database and application helpers
├── database/
│   ├── data/
│   │   ├── sessions.csv         # Study session data
│   │   └── study.db             # SQLite database
│   └── sql/
│       └── schema.sql           # Database schema
└── README.md
```

---

## Dashboard Preview

*(Add your own dashboard screenshots here)*

---

## Installation & Setup

```bash
# Unzip the project folder and navigate into it
cd ai-study-tracker

# Set up a virtual environment
python -m venv .venv
# Windows
.venv\Scripts\activate
# macOS/Linux
source .venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Launch the dashboard
streamlit run frontend/streamlit_app.py
```

**Note:**
1. Upon first launch, the database (`database/data/study.db`) will be automatically initialized.
2. Use the **Register** tab to create a new account.
3. Log in to start tracking your study sessions!

### Backend Commands

Run these commands from the project root. Each script has project-relative
defaults, so no path arguments are required for the standard workflow:

```bash
# Generate synthetic sessions
python backend/src/generate_sample.py

# Load the generated CSV into SQLite
python backend/src/ingest.py

# Train or retrain the productivity model
python backend/src/train_model.py
```

---

## Tech Stack

| Layer | Technology |
|:--|:--|
| **Frontend** | Streamlit + Plotly |
| **Backend** | Python application and ML pipeline |
| **Database** | SQLite and SQL schema scripts |
| **Security** | SHA-256 Hashing, Session State Management |
| **ML Model** | RandomForestRegressor (scikit-learn) |
| **Data Handling** | pandas, SQLAlchemy |
| **Language** | Python 3.10+ |

---

## Key Features

- **Secure Login/Register System**: Multi-user support with password hashing (SHA-256).
- **User-specific Data Isolation**: Each user sees only their own study sessions.
- **Advanced Analytics**:
    - Mood vs Productivity (Scatter Plot)
    - Productivity Distribution by Technique (Box Plot)
    - Caffeine vs Productivity (Scatter Plot)
    - Distribution of Study Session Lengths (Histogram)
- Log daily study sessions with mood, distractions, caffeine, and techniques  
- Predict productivity with ML model  
- Visualize time trends and subject-wise averages  
- Local SQLite database (portable and private)  
- Add new sessions interactively via the Streamlit sidebar  
- Estimate productivity in real-time  

---

## Data Schema

### Users Table
| Column | Description |
|:--|:--|
| `user_id` | Primary Key |
| `username` | Unique username |
| `password_hash` | SHA-256 hashed password |
| `created_at` | Timestamp of registration |

### Study Sessions Table
| Column | Description |
|:--|:--|
| `session_id` | Primary Key |
| `user_id` | Foreign Key linking to Users table |
| `date` | Session date (YYYY-MM-DD) |
| `start_time` / `end_time` | HH:MM 24h format |
| `duration_min` | Computed from start–end times |
| `subject` | Math, Physics, CS, Biology, History |
| `technique` | Pomodoro, Active Recall, etc. |
| `distractions` | Number of interruptions |
| `mood` | 1-5 scale |
| `caffeine_mg` | Caffeine intake (mg) |
| `productivity` | Self-rated (1-5) |

---

## Machine Learning

The app uses **RandomForestRegressor** from `scikit-learn` trained on historical study logs.

**Features used for prediction:**
- Duration (minutes)
- Subject
- Technique
- Distractions
- Mood
- Caffeine (mg)

**Target:**
- Productivity (1–5 scale)

The model is modular, you can upgrade it to **XGBoost** or **Neural Networks**.

---

## Example Insights

- Productivity tends to **increase with mood** and **decrease with distractions**  
- “Active Recall” and “Spaced Repetition” correlate with higher productivity  
- Optimal caffeine range: 100–200 mg  

---

## UI Highlights

- **Login Page**: Professional library background with secure authentication.
- Clean, interactive Streamlit interface  
- Real-time productivity estimation  
- KPI tiles for total minutes, average mood, and average productivity  
- Line chart: *Study Minutes Over Time*  
- Bar chart: *Average Productivity by Subject*  
- Scatter plot: *Mood vs Productivity*
- Box plot: *Productivity Distribution by Technique*
- Scatter plot: *Caffeine vs Productivity*
- Histogram: *Distribution of Study Session Lengths*  

---

## Developed By

**[Your Name]**  
*MCA Final Year Project*
