import streamlit as st
import pandas as pd
from datetime import datetime
import os

# --- APP CONFIG & DATA ---
st.set_page_config(page_title="GymFlow", layout="wide")

# Exercise Library (Your Program)
PROGRAM = {
    "Monday": ["Deadlift", "Shoulder Press", "Barbell Row", "Push Ups", "Bicep Curls", "Russian Twist"],
    "Wednesday": ["Sumo Deadlift", "Back Squat", "Pull Down Cable", "Seated Cable Row", "Cable Palloff Press", "Tricep Cable", "Plank"],
    "Friday": ["Front Squat", "RDL", "Seated DB Press", "DB Bench Press", "Side Plank", "Hollow Hold", "Superhuman"]
}

# Load or create local storage
DB_FILE = "workout_logs.csv"
if not os.path.exists(DB_FILE):
    df = pd.DataFrame(columns=["Date", "Day", "Exercise", "Weight", "Reps", "1RM"])
    df.to_csv(DB_FILE, index=False)

def log_data(day, exercise, weight, reps):
    one_rm = round(weight * (1 + (reps / 30)), 1)
    new_entry = pd.DataFrame([[datetime.now().strftime("%Y-%m-%d"), day, exercise, weight, reps, one_rm]], 
                             columns=["Date", "Day", "Exercise", "Weight", "Reps", "1RM"])
    new_entry.to_csv(DB_FILE, mode='a', header=False, index=False)

# --- HOME PAGE LOGIC ---
st.title("💪 My Training Lab")

# 1. Auto-select based on actual day
current_day_name = datetime.now().strftime("%A")
default_day = current_day_name if current_day_name in PROGRAM else "Monday"

selected_day = st.radio("Select Training Day:", ["Monday", "Wednesday", "Friday"], index=["Monday", "Wednesday", "Friday"].index(default_day), horizontal=True)

st.divider()

# 2. Display Exercises for the Selected Day
st.subheader(f"Today's Plan: {selected_day}")

# Create a clean input form for the day
for ex in PROGRAM[selected_day]:
    with st.expander(f"➔ {ex}", expanded=True):
        col1, col2, col3 = st.columns([2, 2, 1])
        
        with col1:
            w = st.number_input(f"Weight (kg)", key=f"w_{ex}", step=2.5, min_value=0.0)
        with col2:
            r = st.number_input(f"Reps", key=f"r_{ex}", step=1, min_value=0)
        with col3:
            st.write(" ") # Padding
            if st.button("Log", key=f"btn_{ex}"):
                log_data(selected_day, ex, w, r)
                st.toast(f"Saved: {ex} @ {w}kg")

# --- PROGRESS TRACKER ---
st.divider()
if st.checkbox("Show Progress History"):
    history_df = pd.read_csv(DB_FILE)
    if not history_df.empty:
        st.dataframe(history_df.tail(10), use_container_width=True)
        # Simple Chart
        st.line_chart(history_df, x="Date", y="1RM")
    else:
        st.write("No logs yet. Go lift something!")