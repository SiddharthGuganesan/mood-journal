import csv
from datetime import datetime
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
def detect(text):
    text = text.lowet()
    for mood, keywords in moodkey.items():
        for word in keywords:
            if word in text:
                return mood
    return "Neutral"
def entry():
    print("\n~ M O O D J O U R N A L ~")
    print("\nHiii!, How are you feeling today? \n \nChoose an option:")
    print("\n1. Happy/great/awesome/joy")
    print("2. Sad/down/cry/bad")
    print("3. Angry/mad/annoyed")
    print("4. Neutral/okay/fine")

    choice = input("\n Enter the number (1-4): ").strip()

    moodmap = { "1" : "Happy", "2" : "Sad", "3" : "Angry", "4" : "Neutral"}
    mood = moodmap.get(choice)

    if not mood:
        print("Oops! Invalid choice. Please try again")
        return
    entry = input("\nWrite a short note for yourself <3: ")
    now = datetime.now()
    date = now.strftime("%d-%m-%Y")
    time = now.strftime("%I:%M:%p")
    print("today..",date)
    print("time..",time)

    with open ("moodlog.csv",mode="a",newline='') as file:
        writer = csv.writer(file)
        print('\n')
        writer.writerow([date,time,mood,entry])

        quote=random.choice(motqots[mood])

        print(f"\n Mood selected: {mood}")
        print(f" Your entry has been saved!")
        print(f"\nHere's something for you <3:\n \n \"{quote}\"\n")

        print("\n =======================================================================")
#==============================================================================================
def view():
    print("\n Your mood journal entries:")

    try:
        with open("moodlog.csv",mode="r") as file:
            reader = csv.reader(file)
            has_entries = False
            for row in reader:
                if row:
                    print(f" DATE: {row[0]} | TIME: {row[1]} | MOOD: {row[2]} | NOTE: {row[3]}")
                    has_entries = True

            if not has_entries:
                print(" No entries found!")

    except FileNotFoundError:
        print(" You haven't looged any moods yet.")
        
import matplotlib.pyplot as plt

def plot():
    values = {"Angry": 0, "Sad": 1, "Neutral": 2, "Happy": 3}
    dates = []
    score = []

    try:
        with open("moodlog.csv", mode ="r") as file:
            reader = csv.reader(file)
            for row in reader:
                if row:
                    date = row[0]
                    mood = row[2]
                    if mood in values:
                        dates.append(date)
                        score.append (values[mood])
        if not dates:
            print("No data to plot.")
            return

        plt.figure(figsize=(10,5))
        plt.plot (dates, score, marker='o', linestyle='-', color='purple')
        plt.yticks([0,1,2,3],["Angry","Sad","Neutral","Happy"])
        plt.xlabel("Date")
        plt.ylabel("Mood")
        plt.title("Mood trend over time")
        plt.xticks(rotation=45)
        plt.tight_layout()
        plt.grid(True)
        plt.show()

    except FileNotFoundError:
        print("NO mood log file found")



from collections import Counter

def pie():
    try:
        with open ("moodlog.csv",'r') as file:
            reader = csv.reader(file)
            moods = [row[1] for row in reader if row]

        if len(moods)== 0:
            print("No mood data found to plot.")
            return

        moodcount = Counter(moods)

        labels = moodcount.keys()
        sizes = moodcount.values()
        colors = ['lightgreen','lightskyblue','lightcoral','lightred']
        explode = [0.05]*len(labels)

        plt.figure(figsize=(6,6))
        plt.pie(sizes,labels=labels,colors=colors,explode=explode,autopct="%1.1f%%",startangle =140)
        plt.title("Mood Distribution")
        plt.axis("equal")
        plt.show()

    except FileNotFoundError:
        print("No mood log file found. please log some mods first")
                        









    









        
