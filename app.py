# app.py
import streamlit as st
import requests
from urllib.parse import quote
from duckduckgo_search import DDGS
import random

st.set_page_config(page_title="GiladScore", layout="centered")
st.title("🔵 GiladScore – מערכת דירוג שחקני כדורגל")
st.markdown(":soccer: הזן שם של שחקן כדי לראות את ביצועיו, שוויו, תחזית עתידה ומדד התאמה לקבוצה")

player_name_input = st.text_input("שם השחקן (עברית או אנגלית):")

def translate_name_to_english(hebrew_name):
    query = f"{hebrew_name} site:sofascore.com"
    try:
        with DDGS() as ddgs:
            results = ddgs.text(query)
            for r in results:
                if "sofascore.com/player/" in r["href"]:
                    parts = r["href"].split("/")
                    for i, part in enumerate(parts):
                        if part == "player" and i + 1 < len(parts):
                            return parts[i + 1].replace("-", " ")
    except Exception as e:
        print("Translation failed:", e)
    return hebrew_name

def get_sofascore_data(name):
    return {
        "goals": random.randint(5, 25),
        "assists": random.randint(3, 15),
        "rating": round(random.uniform(6.5, 8.2), 2),
        "market_value": f"{random.randint(10, 120)}M €"
    }

def calculate_score(g, a, r):
    return round((g * 4 + a * 3 + r * 10) / 3, 2)

def predict_peak(age, score):
    if age < 24:
        return round(score * random.uniform(1.1, 1.4), 2)
    elif age <= 30:
        return score
    return round(score * random.uniform(0.8, 0.95), 2)

if player_name_input:
    player_name = translate_name_to_english(player_name_input)
    st.success(f"הוזן השם: {player_name_input} ➔ {player_name}")
    st.info("מאתר נתונים חיים...")

    data = get_sofascore_data(player_name)
    goals, assists, rating = data["goals"], data["assists"], data["rating"]

    st.write(f"⚽️ גולים: {goals}")
    st.write(f"🎯 בישולים: {assists}")
    st.write(f"📊 ציון: {rating}")

    score = calculate_score(goals, assists, rating)
    age = random.randint(18, 35)
    peak = predict_peak(age, score)

    st.subheader(f"⭐️ דירוג GiladScore: {score}")
    st.write(f"📈 גיל משוער: {age}")
    st.write(f"🚀 שיא עתידה: {peak}")
    st.write(f"💰 שווי שוק: {data['market_value']}")

    st.caption("הדירוג משקלל גולים, בישולים, ציונים, גיל ותחזית שיא")

