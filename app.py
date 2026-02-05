import streamlit as st
import pandas as pd
from datetime import datetime
import os
import time

# --- APP CONFIG ---
st.set_page_config(page_title="GymFlow", layout="wide")

# Program Library with Target Sets explicitly defined
PROGRAM = {
    "Monday": {
        "Deadlift": {"w": 80.0, "r": 10, "s": 4, "note": "Superset: Shoulder Press"},
        "Shoulder Press": {"w": 20.0, "r": 15, "s": 2, "note": "2x15"},
        "Barbell Row": {"w": 30.0, "r": 10, "s": 4, "note": "4x10"},
        "Push Ups": {"w": 0.0, "r": 10, "s": 4, "note": "4x10"},
        "Bicep Curls": {"w": 12.5, "r": 10, "s": 4, "note": "4x10"},
        "Russian Twist": {"w": 5.0, "r": 10, "s": 4, "note": "5kg plate"}
    },
    "Tuesday": {
        "LISS Cardio": {"w": 0.0, "r": 45, "s": 1, "note": "Incline Walk"}
    },
    "Wednesday": {
        "Sumo Deadlift": {"w": 60.0, "r": 10, "s": 4, "note": "4x10"},
        "Back Squat": {"w": 50.0, "r": 10, "s": 4, "note": "4x10"},
        "Pull Down Cable": {"w": 30.0, "r": 10, "s": 4, "note": "4x10"},
        "Seated Cable Row": {"w": 30.0, "r": 10, "s": 4, "note": "4x10"},
        "Cable Palloff Press": {"w": 10.0, "r": 10, "s": 4, "note": "4x10"},
        "Tricep Cable": {"w": 15.0, "r": 10, "s": 4, "note": "4x10"},
        "Plank": {"w": 0.0, "r": 120, "s": 1, "note": "Collect 2 mins"}
    },
    "Thursday": {
        "Intervals": {"w": 0.0, "r": 30, "s": 1, "note": "Bike/Ski/Row"}
    },
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
    df = pd.DataFrame(columns=["Date", "Day", "Exercise", "Weight", "Reps", "Set_Number", "1RM"])
    df.to_csv(DB_FILE, index=False)

if 'set_tracker' not in st.session_state:
    st.session_state.set_tracker = {}

def log_data(day, exercise, weight, reps, set_num):
    one_rm = round(weight * (1 + (reps / 30)), 1) if reps > 0 else 0
    new_entry = pd.DataFrame([[datetime.now().strftime("%Y-%m-%d %H:%M"), day, exercise, weight, reps, set_num, one_rm]], 
                             columns=["Date", "Day", "Exercise", "Weight", "Reps", "Set_Number", "1RM"])
    new_entry.to_csv(DB_FILE, mode='a', header=False, index=False)

# --- UI ---
st.title("💪 My Training Lab")

all_days = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
current_day_name = datetime.now().strftime("%A")
selected_day = st.radio("Select Day:", all_days, index=all_days.index(current_day_name) if current_day_name in all_days else 0, horizontal=True)

st.divider()

if selected_day in PROGRAM:
    for ex, info in PROGRAM[selected_day].items():
        if ex not in st.session_state.set_tracker:
            st.session_state.set_tracker[ex] = 0
            
        done_sets = st.session_state.set_tracker[ex]
        total_sets = info['s']
        
        # UI logic for the header
        status_icon = "⏳" if done_sets < total_sets else "✅"
        with st.expander(f"{status_icon} {ex} — {done_sets} / {total_sets} Sets Complete", expanded=(done_sets < total_sets)):
            
            # Visual Progress Bar
            progress = done_sets / total_sets
            st.progress(progress)
            st.write(f"**Target:** {total_sets} sets of {info['r']} reps @ {info['w']}kg")
            st.caption(f"Note: {info['note']}")
            
            col1, col2, col3 = st.columns([2, 2, 1])
            with col1:
                w_input = st.number_input(f"Weight (kg)", key=f"w_{ex}", step=2.5, value=float(info['w']))
            with col2:
                r_input = st.number_input(f"Reps", key=f"r_{ex}", step=1, value=int(info['r']))
            with col3:
                st.write(" ")
                if st.button(f"Log Set {done_sets + 1}", key=f"btn_{ex}", disabled=(done_sets >= total_sets)):
                    st.session_state.set_tracker[ex] += 1
                    log_data(selected_day, ex, w_input, r_input, st.session_state.set_tracker[ex])
                    st.rerun() # Refresh to update the progress bar immediately

else:
    st.info("Rest Day! Focus on recovery.")

# --- HISTORY ---
if st.checkbox("Show Progress History"):
    if os.path.exists(DB_FILE):
        history_df = pd.read_csv(DB_FILE)
        st.dataframe(history_df.tail(15), use_container_width=True)
