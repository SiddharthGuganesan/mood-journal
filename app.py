import streamlit as st
import csv
import os
from datetime import datetime
import matplotlib.pyplot as plt
from collections import Counter
import random

# ------------------ DATA ------------------ #
moodkey = {
    "Happy": ["happy", "great", "cool", "awesome", "joy", "excited", "😊", "😄", "😀"],
    "Sad": ["sad", "down", "bad", "depressed", "cry", "😞", "😢"],
    "Angry": ["angry", "mad", "furious", "annoyed", "😠", "😡"],
    "Neutral": ["okay", "fine", "normal", "meh"]
}

motqots = {
    "Happy": ["Keep Shining!!", "Multiply the joy you have!!", "Happiness looks great on you!"],
    "Sad": ["This too shall pass, do not worry", "You are stronger than you think", "It's okay to not be okay"],
    "Angry": ["Take a breath... you’ve got this!", "Don't let anger win your day", "Pause. Reflect. Restart."],
    "Neutral": ["Even ordinary days build extraordinary lives", "Balance is beautiful", "Stay grounded and keep going..."]
}

# ------------------ PASSWORD CHECK ------------------ #
def password_gate():
    st.header("🔐 Mood Journal Login")
    passwordfile = "password.txt"

    if not os.path.exists(passwordfile):
        new = st.text_input("Create a new password", type="password")
        confirm = st.text_input("Confirm password", type="password")
        if st.button("Set Password"):
            if new == confirm and new != "":
                with open(passwordfile, 'w') as f:
                    f.write(new)
                st.success("Password created! Reload to log in.")
            else:
                st.error("Passwords do not match or are empty.")
        st.stop()

    saved = open(passwordfile).read()
    entered = st.text_input("Enter your password", type="password")
    if entered != saved:
        st.warning("Please enter the correct password to continue.")
        st.stop()
    else:
        st.success("Access granted ✅")

# ------------------ ENTRY ------------------ #
def entry():
    st.subheader("📝 Log Your Mood")
    mood = st.selectbox("How are you feeling today?", list(moodkey.keys()))
    note = st.text_input("Write a short note (optional)")
    if st.button("Log Mood"):
        now = datetime.now()
        date = now.strftime("%d-%m-%Y")
        time = now.strftime("%I:%M %p")
        with open("moodlog.csv", "a", newline='') as file:
            writer = csv.writer(file)
            writer.writerow([date, time, mood, note])
        quote = random.choice(motqots[mood])
        st.success(f"Mood '{mood}' logged on {date} at {time}")
        st.info(f"💬 Quote for you: _{quote}_")

# ------------------ VIEW ------------------ #
def view():
    st.subheader("📖 View Past Entries")
    try:
        with open("moodlog.csv", "r") as file:
            reader = csv.reader(file)
            data = list(reader)
        if data:
            for row in data:
                st.write(f"📅 {row[0]} 🕒 {row[1]} | 😌 {row[2]} | 📝 {row[3]}")
        else:
            st.info("No entries found yet.")
    except FileNotFoundError:
        st.error("No mood log found yet.")

# ------------------ PIE CHART ------------------ #
def pie():
    st.subheader("📊 Mood Distribution Pie Chart")
    try:
        with open("moodlog.csv", "r") as file:
            reader = csv.reader(file)
            moods = [row[2] for row in reader if row]

        if len(moods) == 0:
            st.warning("No mood data found.")
            return

        moodcount = Counter(moods)
        labels = moodcount.keys()
        sizes = moodcount.values()
        explode = [0.05] * len(labels)

        fig, ax = plt.subplots()
        ax.pie(sizes, labels=labels, explode=explode, autopct="%1.1f%%", startangle=140)
        ax.axis("equal")
        st.pyplot(fig)

    except FileNotFoundError:
        st.error("No mood log file found. Please log some moods first.")

# ------------------ MOOD TREND GRAPH ------------------ #
def plot():
    st.subheader("📈 Mood Trend Over Time")
    mood_value = {"Angry": 0, "Sad": 1, "Neutral": 2, "Happy": 3}
    dates = []
    scores = []

    try:
        with open("moodlog.csv", "r") as file:
            reader = csv.reader(file)
            for row in reader:
                if row and row[2] in mood_value:
                    dates.append(row[0])
                    scores.append(mood_value[row[2]])

        if not dates:
            st.info("No mood data to plot.")
            return

        fig, ax = plt.subplots(figsize=(10, 5))
        ax.plot(dates, scores, marker='o', linestyle='-', color='purple')
        ax.set_yticks([0, 1, 2, 3])
        ax.set_yticklabels(["Angry", "Sad", "Neutral", "Happy"])
        ax.set_xlabel("Date")
        ax.set_ylabel("Mood")
        ax.set_title("Mood Trend Over Time")
        plt.xticks(rotation=45)
        ax.grid(True)
        st.pyplot(fig)

    except FileNotFoundError:
        st.error("Mood log file not found.")

# ------------------ MAIN ------------------ #
password_gate()

st.title("🌈 Mood Journal Dashboard")
st.markdown("Track your emotions, reflect, and grow 🌱")

menu = st.radio("Select an option", ["📝 Write Entry", "📖 View Entries", "📊 Mood Pie", "📈 Mood Graph"])

if menu == "📝 Write Entry":
    entry()
elif menu == "📖 View Entries":
    view()
elif menu == "📊 Mood Pie":
    pie()
elif menu == "📈 Mood Graph":
    plot()
