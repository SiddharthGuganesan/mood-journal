import streamlit as st
import csv
from datetime import datetime
import matplotlib.pyplot as plt
from collections import Counter
import random

moodkey = { "Happy" : ["happy","great", "cool", "awesome", "joy" , "excited", "😊", "😄", "😀"],
            "Sad" : ["sad", "down", "bad" , "depressed", "cry", "😞", "😢"],
            "Angry" : ["angry","mad","furious", "annoyed",  "😠", "😡"],
            "Neutral" : [ "okay", "fine", "normal", "meh"]
            }
motqots = { "Happy" : ["Keep Shining!!", "Multiply the joy you have!!", "Happiness looks great on you!"],
            "Sad" : [ "This too shall pass, do not worry", "You are stronger than you think" , "It' okay to not be okay"],
            "Angry" : [ "Take a breath.. you have got this!!!", "Don't let anger win your day", "Pause. Reflect. Restart"],
            "Neutral" : ["Even ordinary days build extraordinary lives","Balance is beautiful ","Stay grounded and keep going....."]
            }
st.title(" -M-O-O-D- -J-O-U-R-N-A-L- ")
st.markdown (" Log how you feel today and get a quote based on your mood!")

selected_mood_display = st.selectbox("How are you feeling today?",list(moodkey.keys()))
selected_mood = moodkey[selected_mood_display]


note = st.text_input("Add a short note (optional):")


if st.button("Log My Mood"):
    today = datetime.now().strftime("%d-%m-%Y")
    with open("moodlog.csv", "a", newline='') as file:
        writer = csv.writer(file)
        writer.writerow([today, selected_mood,note])
    quote = random.choice(motqots[selected_mood])
    st.success(f"Mood logged: {selected_mood}")
    st.info(f" Here's a quote for you: \n> _{quote}_")

if st.button("Show Mood Pie Chart"):
    try:
        with open("moodlog.csv", "r") as file:
            reader = csv.reader(file)
            moods_logged = [row[1] for row in reader if row]

        mood_counts = Counter(moods_logged)
        labels = mood_counts.keys()
        sizes = mood_counts.values()
        fig, ax = plt.subplots()
        ax.pie(sizes, labels=labels, autopct="%1.1f%%", startangle=90)
        ax.axis('equal')
        st.pyplot(fig)
    except:
        st.error("No data found yet. Please log some moods first.")
