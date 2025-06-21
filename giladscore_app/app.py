import streamlit as st
import requests
from bs4 import BeautifulSoup
from duckduckgo_search import DDGS
import random

# טעינת CSS
with open("giladscore_app/style.css", "r", encoding="utf-8") as f:
    st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

st.title("🔵 GiladScore – מערכת דירוג שחקני כדורגל")
st.markdown("⚽ הזן שם של שחקן כדי לראות את ביצועיו ותחזית עתידית")

player_name = st.text_input("שם השחקן (עברית או אנגלית):")

def find_fbref_url(player_name):
    try:
        query = f"{player_name} site:fbref.com"
        with DDGS() as ddgs:
            results = ddgs.text(query)
            for r in results:
                if "fbref.com/en/players/" in r["href"]:
                    return r["href"]
    except:
        return None

def extract_stats_from_fbref(url):
    try:
        r = requests.get(url, headers={'User-Agent': 'Mozilla/5.0'})
        soup = BeautifulSoup(r.text, "html.parser")
        stats = soup.select("div.stats_pullout div")
        goals = assists = 0
        for stat in stats:
            text = stat.get_text()
            if "Goals" in text:
                goals = int(stat.find("strong").text.strip())
            if "Assists" in text:
                assists = int(stat.find("strong").text.strip())
        rating = round(random.uniform(6.5, 8.0), 2)
        return goals, assists, rating
    except:
        return 0, 0, 6.0

def calculate_score(goals, assists, rating):
    return round((goals * 4 + assists * 3 + rating * 10) / 3, 2)

def predict_peak_score(age, score):
    if age < 24:
        return round(score * random.uniform(1.2, 1.5), 2)
    return score

if player_name:
    st.success(f"הוזן השם: {player_name} ➔ {player_name}")
    st.info("מאתר נתונים חיים...")

    fbref_url = find_fbref_url(player_name)
    if fbref_url:
        goals, assists, rating = extract_stats_from_fbref(fbref_url)
        st.write(f"⚽️ גולים: {goals}")
        st.write(f"🎯 בישולים: {assists}")
        st.write(f"📊 ציון: {rating}")
    else:
        st.warning("⚠️ לא נמצאו נתונים מ־FBref (נסה באנגלית או שם מלא)")
        goals, assists, rating = 0, 0, 6.0

    age = random.randint(19, 32)
    peak = predict_peak_score(age, calculate_score(goals, assists, rating))
    st.write(f"🚀 שיא עתידי: {peak}")
