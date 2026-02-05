import streamlit as st
import pandas as pd
from datetime import datetime
import os
import time

# --- APP CONFIG & DATA ---
st.set_page_config(page_title="GymFlow", layout="wide")

# Updated Library with ALL days and Target Values
# Format: "Exercise Name": [Target Weight, Target Reps, "Note"]
PROGRAM = {
    "Monday": {
        "Deadlift": [80.0, 10, "4x10 - Superset with Shoulder Press"],
        "Shoulder Press": [20.0, 15, "2x15"],
        "Barbell Row": [30.0, 10, "4x10"],
        "Push Ups": [0.0, 10, "4x10"],
        "Bicep Curls": [12.5, 10, "4x10"],
        "Russian Twist": [5.0, 10, "4x10 - 5kg plate"]
    },
    "Tuesday": {
        "LISS Cardio": [0.0, 45, "Incline Walk - Zone 2-3"]
    },
    "Wednesday": {
        "Sumo Deadlift": [60.0, 10, "4x10"],
        "Back Squat": [50.0, 10, "4x10"],
        "Pull Down Cable": [30.0, 10, "4x10"],
        "Seated Cable Row": [30.0, 10, "4x10"],
        "Cable Palloff Press": [10.0, 10, "4x10"],
        "Tricep Cable": [15.0, 10, "4x10"],
        "Plank": [0.0, 120, "Collect 2 minutes total"]
    },
    "Thursday": {
        "Intervals (Bike/Ski/Row)": [0.0, 30, "5 min each x 2 OR 6x1min sprints"]
    },
    "Friday": {
        "Front Squat": [40.0, 10, "KB or Barbell (4x10)"],
        "RDL": [12.5, 8, "DB focus (4x8)"],
        "Seated DB Press": [15.0, 6, "Increase kg (4x6)"],
        "DB Bench Press": [17.5, 4, "4x4"],
        "Side Plank": [0.0, 3, "5x3 reps/holds"],
        "Push Ups": [0.0, 10, "Bodyweight"],
        "Hollow Hold": [0.0, 120, "2 mins total"]
    },
    "Saturday": {
        "Rest / Active Recovery": [0.0, 0, "Walk or Mobility work"]
    },
    "Sunday": {
        "Rest Day": [0.0, 0, "Prep for Monday!"]
    }
}

DB_FILE = "workout_logs.csv"
if not os.path.exists(DB_FILE):
    df = pd.DataFrame(columns=["Date", "Day", "Exercise", "Weight", "Reps", "1RM"])
    df.to_csv(DB_FILE, index=False)

def log_data(day, exercise, weight, reps):
    one_rm = round(weight * (1 + (reps / 30)), 1) if reps > 0 else 0
    new_entry = pd.DataFrame([[datetime.now().strftime("%Y-%m-%d"), day, exercise, weight, reps, one_rm]], 
                             columns=["Date", "Day", "Exercise", "Weight", "Reps", "1RM"])
    new_entry.to_csv(DB_FILE, mode='a', header=False, index=False)

# --- APP INTERFACE ---
st.title("💪 My Training Lab")

current_day_name = datetime.now().strftime("%A")
all_days = list(PROGRAM.keys())
selected_day = st.radio("Select Training Day:", all_days, index=all_days.index(current_day_name), horizontal=True)

st.divider()

st.subheader(f"Today's Plan: {selected_day}")

# Display Exercises with Pre-filled Targets
for ex, targets in PROGRAM[selected_day].items():
    target_w, target_r, note = targets
    
    with st.expander(f"➔ {ex} ({note})", expanded=True):
        col1, col2, col3 = st.columns([2, 2, 1])
        
        with col1:
            # Defaults to your spreadsheet weight
            w = st.number_input(f"Weight (kg)", key=f"w_{ex}", step=2.5, value=float(target_w))
        with col2:
            # Defaults to your spreadsheet reps
            r = st.number_input(f"Reps", key=f"r_{ex}", step=1, value=int(target_r))
        with col3:
            st.write(" ") 
            if st.button("Log", key=f"btn_{ex}"):
                log_data(selected_day, ex, w, r)
                st.success("Set Logged!")
                # --- NEW: REST TIMER ---
                with st.empty():
                    for seconds in range(60, 0, -1):
                        st.warning(f"⏱️ Rest: {seconds}s")
                        time.sleep(1)
                    st.write("✔️ Ready for next set!")

# --- HISTORY ---
st.divider()
if st.checkbox("Show Progress History"):
    if os.path.exists(DB_FILE):
        history_df = pd.read_csv(DB_FILE)
        st.dataframe(history_df.tail(10), use_container_width=True)
