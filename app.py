import streamlit as st import requests from bs4 import BeautifulSoup from duckduckgo_search import DDGS from pathlib import Path

st.set_page_config(page_title="GiladScore", layout="centered")

--- Load custom CSS ---

with open("style.css") as f: st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

st.title("\U0001F535 GiladScore – מערכת דירוג שחקני כדורגל") st.markdown("⚽ הזן שם של שחקן כדי לראות את ביצועיו ושוויו העדכני")

player_name = st.text_input("\nשם השחקן (עברית או אנגלית):")

--- חיפוש כתובת FBref ---

def find_fbref_url(player_name): query = f"{player_name} site:fbref.com" with DDGS() as ddgs: for r in ddgs.text(query): if "fbref.com/en/players/" in r["href"]: return r["href"] return None

--- חיפוש כתובת Transfermarkt ---

def find_transfermarkt_url(player_name): query = f"{player_name} site:transfermarkt.com" with DDGS() as ddgs: for r in ddgs.text(query): if "transfermarkt.com" in r["href"] and "/profil/" in r["href"]: return r["href"] return None

--- שליפת נתונים FBref ---

def extract_stats_from_fbref(url): try: r = requests.get(url, headers={'User-Agent': 'Mozilla/5.0'}) soup = BeautifulSoup(r.text, "html.parser") stats = soup.select("div.stats_pullout div") goals = assists = 0 rating = 7.0  # סימולציה לציון for stat in stats: text = stat.get_text() if "Goals" in text: goals = int(stat.find("strong").text.strip()) if "Assists" in text: assists = int(stat.find("strong").text.strip()) return goals, assists, rating except: return 0, 0, 7.0

--- שליפת שווי שוק Transfermarkt ---

def extract_market_value(url): try: r = requests.get(url, headers={'User-Agent': 'Mozilla/5.0'}) soup = BeautifulSoup(r.text, "html.parser") value_tag = soup.find("div", class_="dataMarktwert") if value_tag: return value_tag.get_text(strip=True) return "לא זמין" except: return "שגיאה"

--- תצוגה ---

if player_name: st.markdown(f"הוזן השם: {player_name}") st.info("מאתר נתונים חיים...")

fbref_url = find_fbref_url(player_name)
tm_url = find_transfermarkt_url(player_name)

goals, assists, rating = 0, 0, 7.0

if fbref_url:
    goals, assists, rating = extract_stats_from_fbref(fbref_url)

col1, col2 = st.columns(2)
with col1:
    st.markdown(f"**⚽ גולים:** {goals}")
    st.markdown(f"**🎯 בישולים:** {assists}")
with col2:
    st.markdown(f"**📊 ציון ממוצע:** {rating}")

if tm_url:
    value = extract_market_value(tm_url)
    st.markdown(f"**💰 שווי שוק (Transfermarkt):** {value}")
else:
    st.warning("⚠️ שווי שוק עדכני לא נמצא")

st.caption("הנתונים מבוססים על מקורות פתוחים בלבד (FBref, Transfermarkt)")
