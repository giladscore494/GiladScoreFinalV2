import streamlit as st
import requests
import random

# הגדרות עמוד
st.set_page_config(page_title="GiladScore", layout="centered")
st.title("🔵 GiladScore – מבוסס SofaScore")
st.markdown("הזן שם של שחקן כדי לראות את ביצועיו ותחזית עתידית.")

player_name = st.text_input("שם שחקן (אנגלית):")

def find_sofascore_player_url(name):
    query = name.replace(" ", "-").lower()
    # נחפש URL מתאים בסוג סטטית (אפשר לשפר בהמשך)
    # דוגמה: https://www.sofascore.com/player/lionel-messi/28003
    # נשתמש ב־Search API של SofaScore (לא רשמי).
    url = f"https://www.sofascore.com/search/v2/player/{query}"
    res = requests.get(url)
    if res.status_code != 200:
        return None
    data = res.json()
    try:
        players = data["player"]
        if players and len(players) > 0:
            return players[0]["url"]
    except:
        return None
    return None

def extract_sofascore_stats(player_url):
    try:
        full_url = "https://www.sofascore.com" + player_url
        res = requests.get(full_url, headers={'User-Agent':'Mozilla/5.0'})
        # נתוני HTML דינמי, יש גריף JSON בטקסט
        prefix = "window.__INITIAL_STATE__ = "
        idx = res.text.find(prefix)
        if idx == -1:
            return None
        json_str = res.text[idx + len(prefix):]
        json_str = json_str.split(";</script>", 1)[0]
        data = requests.utils.json.loads(json_str)
        stats = data["playerPage"]["player"]["statistics"]["seasonGoalsAndAssists"]
        rating = data["playerPage"]["player"]["statistics"]["seasonRating"]
        return stats["goals"], stats["assists"], rating
    except:
        return None

def calculate_score(goals, assists, rating):
    return round((goals * 4 + assists * 3 + rating * 10)/3, 2)

def predict_peak(age, score):
    if age < 24: return round(score*random.uniform(1.1,1.3),2)
    if age <=29: return score
    return round(score*random.uniform(0.85,0.95),2)

if player_name:
    st.info("מאתר שחקן ב‑SofaScore…")
    url = find_sofascore_player_url(player_name)
    if not url:
        st.error("⚠️ לא נמצא שחקן מתאים ב‑SofaScore (נסה באנגלית מלא)")
    else:
        res = extract_sofascore_stats(url)
        if not res:
            st.error("⚠️ לא הצלחנו לשלוף נתונים שוטפים")
        else:
            goals, assists, rating = res
            st.write(f"⚽️ גולים: {goals}")
            st.write(f"🎯 בישולים: {assists}")
            st.write(f"📊 ממוצע דירוג: {rating}")
            score = calculate_score(goals, assists, rating)
            st.subheader(f"⭐️ דירוג GiladScore: {score}")
            age = random.randint(18,35)
            st.write(f"📈 גיל משוער: {age}")
            st.write(f"🚀 תחזית שיא: {predict_peak(age, score)}")
            # שווי שוק – מגירוד HTML של דף Player
            market_tag = extract_sofascore_market(full_url)
            st.write(f"💰 שווי (אם קיים): {market_tag or '— לא נמצא'}")
