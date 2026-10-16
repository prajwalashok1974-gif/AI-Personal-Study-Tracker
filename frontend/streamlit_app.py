from __future__ import annotations
import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[1]
sys.path.append(str(PROJECT_ROOT / 'backend' / 'src'))
import sqlite3, joblib, pandas as pd, streamlit as st, plotly.express as px
from fpdf import FPDF
from utils import ensure_schema, insert_session, register_user, authenticate_user

DB_PATH=PROJECT_ROOT/'database'/'data'/'study.db'
SCHEMA_PATH=PROJECT_ROOT/'database'/'sql'/'schema.sql'
MODEL_PATH=PROJECT_ROOT/'backend'/'models'/'pipeline.joblib'

st.set_page_config(page_title='AI Study Tracker', page_icon='📚', layout='wide')
st.title('📚 AI-Powered Personal Study Tracker')

SUBJECTS = ['css','html','C++','python','java', 'c ', 'js']
TECHNIQUES = ['Timed Study Block','Active Recall','Note-taking','Practice Problems','Spaced Repetition']
CFG={'displayModeBar':True,'responsive':True}

# Initialize Session State
if 'user_id' not in st.session_state:
    st.session_state['user_id'] = None
if 'username' not in st.session_state:
    st.session_state['username'] = None

ensure_schema(DB_PATH, SCHEMA_PATH)

def login_page():
    # Add a background image
    st.markdown(
        """
        <style>
        /* Dark theme background */
        .stApp {
             background-image: url("https://images.unsplash.com/photo-1524995997946-a1c2e315a42f?ixlib=rb-4.0.3&auto=format&fit=crop&w=1920&q=80");
            background-size: cover;
            background-position: center;
            background-repeat: no-repeat;
        }
        /* Form background with a semi-transparent dark color */
        [data-testid="stForm"] {
            background-color: rgba(42, 42, 42, 0.85);
            padding: 25px;
            border-radius: 15px;
            border: 1px solid #444;
        }
        /* Input fields styling */
        [data-testid="stForm"] input[type="text"],
        [data-testid="stForm"] input[type="password"] {
            background-color: #3c3c3c;
            color: #FFFFFF;
            border: 1px solid #555;
            border-radius: 5px;
        }
        /* Text color for headers, tabs, and labels */
        h2, [data-testid="stTabs"] button, [data-testid="stForm"] label {
            color: rgba(255, 255, 255, 0.9) !important;
            font-weight: bold !important;
        }
        /* Active tab styling */
        [data-testid="stTabs"] button[aria-selected="true"] {
            background-color: transparent;
            color: #00bfff !important; /* DeepSkyBlue for active tab */
            border-bottom: 2px solid #00bfff;
        }
        /* Login/Register button styling */
        [data-testid="stForm"] [data-testid="stButton"] > button {
            background-color: #00bfff;
            color: white;
            border: none;
            border-radius: 5px;
            padding: 10px 20px;
            width: 100%;
        }
        </style>
        """,
        unsafe_allow_html=True
    )

    st.subheader("🔐 Login / Register")
    tab1, tab2 = st.tabs(["Login", "Register"])
    
    with tab1:
        with st.form("login_form"):
            username = st.text_input("Username")
            password = st.text_input("Password", type="password")
            submit = st.form_submit_button("Login")
            if submit:
                uid = authenticate_user(DB_PATH, username, password)
                if uid:
                    st.session_state['user_id'] = uid
                    st.session_state['username'] = username
                    st.success(f"Welcome back, {username}!")
                    st.rerun()
                else:
                    st.error("Invalid username or password")

    with tab2:
        with st.form("register_form"):
            new_user = st.text_input("New Username")
            new_pass = st.text_input("New Password", type="password")
            submit_reg = st.form_submit_button("Register")
            if submit_reg:
                if new_user and new_pass:
                    if register_user(DB_PATH, new_user, new_pass):
                        st.success("User registered! Please login.")
                    else:
                        st.error("Username already exists")
                else:
                    st.error("Please fill in all fields")

@st.cache_data(show_spinner=False)
def load_df(user_id: int)->pd.DataFrame:
    if not DB_PATH.exists(): return pd.DataFrame()
    con=sqlite3.connect(DB_PATH)
    try: 
        df=pd.read_sql_query('SELECT * FROM study_sessions WHERE user_id = ?', con, params=(user_id,))
    finally: con.close()
    return df

def load_model():
    if MODEL_PATH.exists(): return joblib.load(MODEL_PATH)
    return None

def create_pdf_report(df: pd.DataFrame, username: str) -> bytes:
    """Generate a PDF report for the user."""
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", "B", 16)
    pdf.cell(40, 10, f"Study Report for {username}")
    pdf.ln(20)
    
    pdf.set_font("Arial", "", 12)
    pdf.cell(40, 10, f"Total Sessions: {len(df)}")
    pdf.ln(10)
    pdf.cell(40, 10, f"Total Minutes: {df['duration_min'].sum()}")
    pdf.ln(10)
    pdf.cell(40, 10, f"Average Productivity: {df['productivity'].mean():.2f}/5")
    pdf.ln(20)
    
    pdf.set_font("Arial", "B", 14)
    pdf.cell(40, 10, "Recent Sessions")
    pdf.ln(10)
    
    pdf.set_font("Arial", "", 10)
    # Table Header
    pdf.cell(30, 10, "Date", 1)
    pdf.cell(30, 10, "Subject", 1)
    pdf.cell(30, 10, "Duration", 1)
    pdf.cell(30, 10, "Productivity", 1)
    pdf.ln()
    
    # Table Rows (Last 10 sessions)
    for _, row in df.tail(10).iterrows():
        pdf.cell(30, 10, str(row['date']), 1)
        pdf.cell(30, 10, str(row['subject']), 1)
        pdf.cell(30, 10, str(row['duration_min']), 1)
        pdf.cell(30, 10, str(row['productivity']), 1)
        pdf.ln()
        
    return pdf.output(dest='S').encode('latin-1')

def main_dashboard():
    # Load data first so we can use it for badges in sidebar
    df=load_df(st.session_state['user_id'])

    st.sidebar.write(f"👤 **{st.session_state['username']}**")
    if st.sidebar.button("Logout"):
        st.session_state['user_id'] = None
        st.session_state['username'] = None
        st.rerun()
        
    with st.sidebar:
        st.header('Add Session')
        with st.form('new_session'):
            date_v=st.date_input('Date')
            start_v=st.time_input('Start time')
            end_v=st.time_input('End time')
            subject_v=st.selectbox('Subject', SUBJECTS)
            technique_v=st.selectbox('Technique', TECHNIQUES)
            distractions_v=st.number_input('Distractions', min_value=0, step=1, value=1)
            mood_v=st.slider('Mood (1-5)',1,5,4)
            caffeine_v=st.number_input('Caffeine (mg)', min_value=0, step=10, value=120)
            productivity_v=st.slider('Productivity (1-5)',1,5,4)
            submitted=st.form_submit_button('Save')
        if submitted:
            try:
                insert_session(DB_PATH, {
                    'date':date_v.isoformat(),
                    'start_time':start_v.strftime('%H:%M'),
                    'end_time':end_v.strftime('%H:%M'),
                    'subject':subject_v,
                    'technique':technique_v,
                    'distractions':int(distractions_v),
                    'mood':int(mood_v),
                    'caffeine_mg':int(caffeine_v),
                    'productivity':int(productivity_v)
                }, st.session_state['user_id'])
                st.success('Session saved ✅'); st.cache_data.clear(); st.rerun()
            except Exception as e: st.error(f'Failed to save session: {e}')

        # Data Export
        st.divider()
        st.subheader("📥 Data Export")
        if not df.empty:
            csv = df.to_csv(index=False).encode('utf-8')
            st.download_button(
                label="Download My Data (CSV)",
                data=csv,
                file_name='my_study_sessions.csv',
                mime='text/csv',
            )
            
            pdf_bytes = create_pdf_report(df, st.session_state['username'])
            st.download_button(
                label="📄 Download Report (PDF)",
                data=pdf_bytes,
                file_name='study_report.pdf',
                mime='application/pdf',
            )

    if df.empty:
        st.info('No data yet. Add sessions using the sidebar.', icon='ℹ️')
    else:
        col1,col2,col3,col4=st.columns(4)
        total_min=int(df['duration_min'].sum()); avg_prod=df['productivity'].mean(); sessions=len(df); avg_mood=df['mood'].mean()
        col1.metric('Total Minutes', f'{total_min:,}'); col2.metric('Sessions', f'{sessions:,}'); col3.metric('Avg Productivity', f'{avg_prod:.2f}'); col4.metric('Avg Mood', f'{avg_mood:.2f}')
        
        st.divider(); left,right=st.columns(2)
        with left:
            by_date=df.groupby('date',as_index=False).agg(minutes=('duration_min','sum'))
            fig=px.line(by_date,x='date',y='minutes',markers=True,title='Study Minutes Over Time')
            st.plotly_chart(fig, config=CFG)
        with right:
            by_subj=df.groupby('subject',as_index=False).agg(avg_prod=('productivity','mean'))
            fig2=px.bar(by_subj,x='subject',y='avg_prod',title='Average Productivity by Subject')
            st.plotly_chart(fig2, config=CFG)

        st.divider()
        st.subheader("📊 Advanced Analytics")
        r2_col1, r2_col2 = st.columns(2)
        with r2_col1:
            fig3 = px.scatter(df, x='mood', y='productivity', color='subject', size='duration_min', 
                            title='Mood vs Productivity (Size = Duration)', hover_data=['technique'])
            st.plotly_chart(fig3, width="stretch", config=CFG)
        with r2_col2:
            fig4 = px.box(df, x='technique', y='productivity', color='technique', title='Productivity Distribution by Technique')
            st.plotly_chart(fig4, width="stretch", config=CFG)

        r3_col1, r3_col2 = st.columns(2)
        with r3_col1:
            fig5 = px.scatter(df, x='caffeine_mg', y='productivity', color='subject', title='Caffeine vs Productivity')
            st.plotly_chart(fig5, width="stretch", config=CFG)
        with r3_col2:
            fig6 = px.histogram(df, x='duration_min', nbins=20, title='Distribution of Study Session Lengths', color='subject')
            st.plotly_chart(fig6, width="stretch", config=CFG)

        st.subheader('All Sessions'); st.dataframe(df.sort_values(['date','start_time']), hide_index=True)
    
    st.divider()
    pipe=load_model(); st.subheader('🔮 Productivity Estimator')
    if pipe is None:
        st.warning('Model not trained yet. Run: `python backend/src/train_model.py` after ingesting data.', icon='⚠️')
    else:
        c1,c2,c3,c4,c5,c6=st.columns(6)
        with c1: sub=st.selectbox('Subject', SUBJECTS, key='pred_sub')
        with c2: tech=st.selectbox('Technique', TECHNIQUES, key='pred_tech')
        with c3: dur=st.number_input('Duration (min)', min_value=10, step=5, value=60, key='pred_dur')
        with c4: dis=st.number_input('Distractions', min_value=0, step=1, value=2, key='pred_dis')
        with c5: mood=st.slider('Mood',1,5,4, key='pred_mood')
        with c6: caf=st.number_input('Caffeine (mg)', min_value=0, step=10, value=100, key='pred_caf')
        df_in=pd.DataFrame([{'duration_min':dur,'subject':sub,'technique':tech,'distractions':dis,'mood':mood,'caffeine_mg':caf}])
        pred=float(pipe.predict(df_in)[0])
        st.metric('Estimated Productivity (1..5)', f'{pred:.2f}')

if st.session_state['user_id'] is None:
    login_page()
else:
    main_dashboard()
