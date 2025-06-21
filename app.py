import streamlit as st

st.set_page_config(page_title="GiladScore", layout="centered")

st.title("🔵 GiladScore – מערכת דירוג שחקני כדורגל")
st.markdown("הזן שם של שחקן כדי לראות את ביצועיו ותחזית עתידית")

player_name = st.text_input("שם השחקן:")

if player_name:
    st.success(f"הוזן השם: {player_name}")
    # כאן תשתלב הפונקציה בעתיד שתביא נתונים
    st.info("כרגע הדירוגים נטענים ממערכת ההערכה... (בהמשך נשלוף מידע חי)")
