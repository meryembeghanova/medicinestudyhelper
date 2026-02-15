import json
from datetime import date, datetime
import time
import random

FILE = "mededu_data.json"

# ---------- DATA ----------

def load_data():
    try:
        with open(FILE, "r") as f:
            return json.load(f)
    except FileNotFoundError:
        return {
            "user": {},
            "topics": []
        }
def save_data(data):
    with open(FILE, "w") as f:
        json.dump(data, f, indent=4)

# ---------- UTILITIES ----------

def get_topic_by_id(data, topic_id):
    for topic in data["topics"]:
        if topic["id"] == topic_id:
            return topic
    return None

# ---------- FEATURES ----------

def welcome():
    print("""
🩺 Welcome to MedEdu Companion!
"Medicine is a science of uncertainty and an art of probability." – William Osler
""")

def create_account():
    data = load_data()
    print("Let's create your account:")
    data["user"]["name"] = input("First Name: ").strip().title()
    data["user"]["surname"] = input("Surname: ").strip().title()
    data["user"]["goal"] = input("Why do you want to study medicine? ").strip()
    save_data(data)
    print(f"\n✅ Account created! Welcome, {data['user']['name']}!\n")

def add_topic():
    data = load_data()
    topic = {
        "id": len(data["topics"]) + 1,
        "name": input("Topic name: ").strip().title(),
        "category": input("Category: ").strip().title(),
        "difficulty": input("Difficulty (Easy/Medium/Hard): ").strip().title(),
        "created_at": str(date.today()),
        "study_sessions": [],
        "notes": [],
        "quiz": {"questions": [], "total_attempts": 0, "best_score": 0}
    }

    # Ask user to create a quiz for this topic
    add_quiz = input("Do you want to add a quiz for this topic? (y/n): ").lower()
    if add_quiz == "y":
        while True:
            question = input("Enter question: ")
            answer = input("Enter answer: ")
            topic["quiz"]["questions"].append({"question": question, "answer": answer})
            more = input("Add another question? (y/n): ").lower()
            if more != "y":
                break

    data["topics"].append(topic)
    save_data(data)
    print("✅ Topic created!")

def log_study():
    data = load_data()
    if not data["topics"]:
        print("❌ No topics yet. Add a topic first.")
        return
    view_dashboard()
    topic_id = int(input("Enter Topic ID to log study: "))
    topic = get_topic_by_id(data, topic_id)
    if not topic:
        print("❌ Topic not found")
        return

    minutes = int(input("Minutes to study (timer will start): "))
    print(f"⏱️ Study timer started for {minutes} minutes...")
    for i in range(minutes):
        time.sleep(1)  # 1 second = 1 minute for demo, change to 60 for real minutes
        print(f"{i + 1}/{minutes} min done...", end="\r")
    print("\n✅ Timer finished! Good job!")

    topic["study_sessions"].append({
        "date": str(date.today()),
        "minutes": minutes
    })
    save_data(data)

def add_note():
    data = load_data()
    if not data["topics"]:
        print("❌ No topics yet. Add a topic first.")
        return
    view_dashboard()
    topic_id = int(input("Enter Topic ID to add note: "))
    topic = get_topic_by_id(data, topic_id)
    if not topic:
        print("❌ Topic not found")
        return

    topic["notes"].append({
        "title": input("Note title: ").strip(),
        "content": input("Note content: ").strip()
    })
    save_data(data)
    print("📝 Note saved!")

def take_quiz():
    data = load_data()
    if not data["topics"]:
        print("❌ No topics yet. Add a topic first.")
        return
    view_dashboard()
    topic_id = int(input("Enter Topic ID to take quiz: "))
    topic = get_topic_by_id(data, topic_id)
    if not topic or not topic["quiz"]["questions"]:
        print("❌ Quiz not available for this topic")
        return

    print(f"\n📝 Starting quiz for {topic['name']}:")
    correct = 0
    for q in topic["quiz"]["questions"]:
        ans = input(q["question"] + " ").strip()
        if ans.lower() == q["answer"].lower():
            correct += 1
    score = int((correct / len(topic["quiz"]["questions"])) * 100)
    print(f"\n✅ You scored {score}%")

    topic["quiz"]["total_attempts"] += 1
    topic["quiz"]["best_score"] = max(topic["quiz"]["best_score"], score)
    save_data(data)

def view_dashboard():
    data = load_data()
    if not data["topics"]:
        print("❌ No topics yet. Add a topic first.")
        return
    print("\n📊 DASHBOARD\n")
    for topic in data["topics"]:
        total_time = sum(s["minutes"] for s in topic["study_sessions"])
        last_date = topic["study_sessions"][-1]["date"] if topic["study_sessions"] else "Never"
        print(f"""
ID: {topic['id']} | {topic['name']}
Category: {topic['category']} | Difficulty: {topic['difficulty']}
Study Time: {total_time} min | Last Studied: {last_date}
Notes: {len(topic['notes'])} | Quiz Best Score: {topic['quiz']['best_score']}%
-----------------------------""")

def suggest_revision():
    data = load_data()
    if not data["topics"]:
        print("❌ No topics yet.")
        return

    # Suggest the topic with least total study time
    topic = min(
        data["topics"],
        key=lambda t: sum(s["minutes"] for s in t["study_sessions"]) if t["study_sessions"] else 0
    )
    print(f"📌 Suggested revision topic: {topic['name']}")

def update_profile():
    data = load_data()
    print("\n👤 Update Profile")
    data["user"]["name"] = input("Enter your name: ").strip().title()
    data["user"]["surname"] = input("Enter your surname: ").strip().title()
    data["user"]["goal"] = input("Enter your study goal: ").strip()
    save_data(data)
    print("✅ Profile updated successfully!")

# ---------- MAIN MENU ----------

def menu():
    welcome()
    data = load_data()
    if not data["user"]:
        create_account()

    while True:
        print(f"""
🧠 MedEdu Companion - Hello {data['user'].get('name', '')}!
1. Set / Update Profile
2. Add Topic
3. Log Study Session
4. Add Note
5. View Dashboard
6. Suggest Revision Topic
7. Take Quiz
8. Exit
""")
        choice = input("Choose: ")

        if choice == "1":
            update_profile()
        elif choice == "2":
            add_topic()
        elif choice == "3":
            log_study()
        elif choice == "4":
            add_note()
        elif choice == "5":
            view_dashboard()
        elif choice == "6":
            suggest_revision()
        elif choice == "7":
            take_quiz()
        elif choice == "8":
            print("👋 See you next time!")
            break
        else:
            print("❌ Invalid choice")
menu()

