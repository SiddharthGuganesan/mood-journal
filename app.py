import streamlit as st
import csv
import os
from datetime import datetime
import matplotlib.pyplot as plt
from collections import Counter
import random

# Mood keywords and motivational quotes
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

# Path for password file
passwordfile = "password.txt"

# Web-based password check
def password_gate():
    st.header("🔐 Welcome to Your Mood Journal")
    
    if not os.path.exists(passwordfile):
        new = st.text_input("Create a new password", type="password")
        confirm = st.text_input("Confirm password", type="password")
        if st.button("Create Password"):
            if new == confirm and new != "":
                with open(passwordfile, 'w') as f:
                    f.write(new)
                st.success("Password created! Reload the app to login.")
            else:
                st.error("Passwords do not match or are empty.")
        st.stop()
    
    saved = open(passwordfile).read()
    entered = st.text_input("Enter your password to continue:", type="password")
    if entered != saved:
        st.warning("Password required to continue.")
        st.stop()
    else:
        st.success("Access granted!")

# Entry function (write mood)
def entry():
    st.subheader(" Write a New Mood Entry")
    selected_mood = st.selectbox("How are you feeling today?", moodkey.keys())
    note = st.text_input("Add a short note (optional):")
    if st.button("Log My Mood"):
        today = datetime.now().strftime("%d-%m-%Y")
        with open("moodlog.csv", "a", newline='') as file:
            writer = csv.writer(file)
            writer.writerow([today, selected_mood, note])
        quote = random.choice(motqots[selected_mood])
        st.success(f"Mood logged: {selected_mood}")
        st.info(f" Quote: _{quote}_")

# View function (see past entries)
def view():
    st.subheader(" Past Mood Entries")
    try:
        with open("moodlog.csv", "r") as file:
            reader = csv.reader(file)
            data = list(reader)
        if not data:
            st.info("No entries found yet.")
        else:
            for row in data:
                st.write(f" {row[0]} |  {row[1]} |  {row[2]}")
    except:
        st.error("Could not read mood log file.")

# Pie chart view
def pie():
    st.subheader(" Mood Pie Chart")
    try:
        with open("moodlog.csv", "r") as file:
            reader = csv.reader(file)
            moods = [row[1] for row in reader if row]
        if not moods:
            st.warning("No mood data found.")
            return
        mood_counts = Counter(moods)
        fig, ax = plt.subplots()
        ax.pie(mood_counts.values(), labels=mood_counts.keys(), autopct="%1.1f%%", startangle=90)
        ax.axis("equal")
        st.pyplot(fig)
    except:
        st.error("Error loading pie chart.")

# Mood graph using bar plot
def plot():
    st.subheader(" Mood Trend (Bar Chart)")
    try:
        with open("moodlog.csv", "r") as file:
            reader = csv.reader(file)
            moods = [row[1] for row in reader if row]
        mood_counts = Counter(moods)
        fig, ax = plt.subplots()
        ax.bar(mood_counts.keys(), mood_counts.values(), color='skyblue')
        ax.set_ylabel("Count")
        ax.set_title("Mood Frequency")
        st.pyplot(fig)
    except:
        st.error("Error loading bar chart.")

# ------------------------ MAIN WEB APP ------------------------ #
password_gate()  # Only allow access if password is correct

st.title("Mood Journal Dashboard")

menu = st.radio("Choose an option:", ["Write Entry", "View Entries", "Show Mood Pie", "Show Mood Graph"])

if menu == "Write Entry":
    entry()
elif menu == "View Entries":
    view()
elif menu == "Show Mood Pie":
    pie()
elif menu == "Show Mood Graph":
    plot()
