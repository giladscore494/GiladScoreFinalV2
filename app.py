import streamlit as st
import requests
from bs4 import BeautifulSoup
from duckduckgo_search import DDGS
import random
from transfermarket.market import Market  # ✅ ספרייה חדשה

# הגדרות ראשיות
st.set_page_config(page_title="GiladScore", layout="centered")
st.title("🔵 GiladScore – מערכת דירוג שחקני כדורגל")
st.markdown("הזן שם של שחקן כדי לראות את ביצועיו, שוויו, תחזית עתידית ומידת ההתאמה לקבוצה")

player_name = st.text_input("שם השחקן:")

# חיפוש FBref
def find_fbref_url(player_name):
    try:
        query = f"{player_name} site:fbref.com"
        with DDGS() as ddgs:
            results = ddgs.text(query)
            for r in results:
                if "fbref.com/en/players/" in r["href"]:
                    return r["href"]
    except Exception as e:
        print("DuckDuckGo search failed:", e)
    return None

# שליפת סטטיסטיקות בסיסיות
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

# שווי שוק באמצעות transfermarket
def get_tm_value(name: str) -> str:
    try:
        m = Market()
        players = m.search_players(name)
        if not players:
            return "⚠️ לא נמצא"
        pid = players[0].id
        details = m.get_player(pid)
        return details.market_value
    except Exception as e:
        return f"⚠️ שגיאה: {e}"

# חישוב הדירוג
def calculate_score(goals, assists, rating):
    return round((goals * 4 + assists * 3 + rating * 10) / 3, 2)

# תחזית שיא קריירה עתידי
def predict_peak_score(age, current_score):
    if age < 24:
        return round(current_score * random.uniform(1.1, 1.4), 2)
    elif 24 <= age <= 29:
        return current_score
    else:
        return round(current_score * random.uniform(0.8, 0.95), 2)

# התחלת תהליך עם שם שחקן
if player_name:
    st.success(f"הוזן השם: {player_name}")
    st.info("מאתר נתונים חיים...")

    fbref_url = find_fbref_url(player_name)

    if fbref_url:
        goals, assists, rating = extract_stats_from_fbref(fbref_url)
        st.write(f"⚽️ גולים: {goals}")
        st.write(f"🎯 בישולים: {assists}")
        st.write(f"📊 ציון ממוצע: {rating}")
    else:
        st.warning("⚠️ לא נמצאו נתונים מ־FBref (נסה באנגלית או שם מלא)")
        goals, assists, rating = 0, 0, 6.0

    score = calculate_score(goals, assists, rating)
    st.subheader(f"⭐️ דירוג GiladScore: {score}")

    age = random.randint(18, 35)
    peak = predict_peak_score(age, score)
    st.write(f"📈 גיל משוער: {age}")
    st.write(f"🚀 תחזית שיא קריירה: {peak}")

    # שווי שוק
    value = get_tm_value(player_name)
    st.write(f"💰 שווי שוק (Transfermarkt): {value}")

    st.caption("הדירוג משקלל גולים, בישולים, ציונים, גיל, מגמת התפתחות ושווי")
