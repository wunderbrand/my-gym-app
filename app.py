import streamlit as st
import pandas as pd
from datetime import datetime
import os
import plotly.express as px

# --- APP CONFIG ---
st.set_page_config(page_title="GymFlow", layout="wide", initial_sidebar_state="collapsed")

# Program Library
PROGRAM = {
    "Monday": {
        "Deadlift": {"w": 80.0, "r": 10, "s": 4, "note": "Superset: Shoulder Press"},
        "Shoulder Press": {"w": 20.0, "r": 15, "s": 2, "note": "2x15"},
        "Barbell Row": {"w": 30.0, "r": 10, "s": 4, "note": "4x10"},
        "Push Ups": {"w": 0.0, "r": 10, "s": 4, "note": "4x10"},
        "Bicep Curls": {"w": 12.5, "r": 10, "s": 4, "note": "4x10"},
        "Russian Twist": {"w": 5.0, "r": 10, "s": 4, "note": "5kg plate"}
    },
    "Tuesday": {"LISS Cardio": {"w": 0.0, "r": 45, "s": 1, "note": "Incline Walk"}},
    "Wednesday": {
        "Sumo Deadlift": {"w": 60.0, "r": 10, "s": 4, "note": "4x10"},
        "Back Squat": {"w": 50.0, "r": 10, "s": 4, "note": "4x10"},
        "Pull Down Cable": {"w": 30.0, "r": 10, "s": 4, "note": "4x10"},
        "Seated Cable Row": {"w": 30.0, "r": 10, "s": 4, "note": "4x10"},
        "Cable Palloff Press": {"w": 10.0, "r": 10, "s": 4, "note": "4x10"},
        "Tricep Cable": {"w": 15.0, "r": 10, "s": 4, "note": "4x10"},
        "Plank": {"w": 0.0, "r": 120, "s": 1, "note": "Collect 2 mins"}
    },
    "Thursday": {"Intervals": {"w": 0.0, "r": 30, "s": 1, "note": "Bike/Ski/Row"}},
    "Friday": {
        "Front Squat": {"w": 40.0, "r": 10, "s": 4, "note": "KB or Barbell"},
        "RDL": {"w": 12.5, "r": 8, "s": 4, "note": "4x8"},
        "Seated DB Press": {"w": 15.0, "r": 6, "s": 4, "note": "4x6"},
        "DB Bench Press": {"w": 17.5, "r": 4, "s": 4, "note": "4x4"},
        "Side Plank": {"w": 0.0, "r": 3, "s": 5, "note": "5x3 reps"},
        "Push Ups": {"w": 0.0, "r": 10, "s": 4, "note": "Bodyweight"},
        "Hollow Hold": {"w": 0.0, "r": 120, "s": 1, "note": "2 mins total"}
    }
}

DB_FILE = "workout_logs.csv"
if not os.path.exists(DB_FILE):
    df = pd.DataFrame(columns=["Date", "Day", "Exercise", "Weight", "Reps", "Sets_Completed", "1RM"])
    df.to_csv(DB_FILE, index=False)

if 'completed_exercises' not in st.session_state:
    st.session_state.completed_exercises = []

def log_bulk_data(day, exercise, weight, reps, total_sets):
    one_rm = round(weight * (1 + (reps / 30)), 1) if reps > 0 else 0
    new_entry = pd.DataFrame([[datetime.now().strftime("%Y-%m-%d"), day, exercise, weight, reps, total_sets, one_rm]], 
                             columns=["Date", "Day", "Exercise", "Weight", "Reps", "Sets_Completed", "1RM"])
    new_entry.to_csv(DB_FILE, mode='a', header=False, index=False)

# --- APP UI ---
st.title("💪 My Training Lab")

all_days = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
current_day_name = datetime.now().strftime("%A")
selected_day = st.radio("Today's Workout:", all_days, index=all_days.index(current_day_name) if current_day_name in all_days else 0, horizontal=True)

st.divider()

if selected_day in PROGRAM:
    for ex, info in PROGRAM[selected_day].items():
        is_done = ex in st.session_state.completed_exercises
        status_icon = "✅" if is_done else "🏋️"
        
        with st.expander(f"{status_icon} {ex}", expanded=(not is_done)):
            st.write(f"**Target:** {info['s']} sets of {info['r']} reps @ {info['w']}kg")
            col1, col2 = st.columns(2)
            with col1:
                w_input = st.number_input(f"Weight (kg)", key=f"w_{ex}", step=2.5, value=float(info['w']))
            with col2:
                r_input = st.number_input(f"Reps", key=f"r_{ex}", step=1, value=int(info['r']))
            
            if st.button(f"Log {info['s']} Sets Complete", key=f"btn_{ex}", use_container_width=True, disabled=is_done):
                log_bulk_data(selected_day, ex, w_input, r_input, info['s'])
                st.session_state.completed_exercises.append(ex)
                st.rerun()
else:
    st.info("Enjoy your rest day!")

# --- PROGRESS VISUALIZER ---
st.divider()
st.subheader("📈 Strength Progress")
if os.path.exists(DB_FILE):
    history_df = pd.read_csv(DB_FILE)
    if not history_df.empty:
        # Create a dropdown to pick which exercise chart to see
        chart_ex = st.selectbox("Select Exercise to View Progress:", history_df["Exercise"].unique())
        filtered_df = history_df[history_df["Exercise"] == chart_ex]
        
        fig = px.line(filtered_df, x="Date", y="Weight", title=f"{chart_ex} Over Time", markers=True)
        st.plotly_chart(fig, use_container_width=True)
    else:
        st.write("Start logging to see your progress charts!")
