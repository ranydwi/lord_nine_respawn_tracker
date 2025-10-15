import streamlit as st
import pandas as pd
from datetime import datetime, timedelta

# ======================
# ⚙️ Konfigurasi Awal
# ======================
st.set_page_config(page_title="Lord Nine Boss Respawn Tracker", layout="centered")

st.title("Lord Nine Boss Respawn Tracker")

# ======================
# 📘 Data Respawn Boss
# ======================
BOSS_RESPAWN = {
    "Viorent": 10,
    "Venatus": 10,
    "Ego": 21,
    "Livera": 24,
    "Araneo": 24,
    "Undomiel": 24,
    "Lady Dalia": 18,
    "Amentis": 29,
    "General": 29,
    "Baron": 32,
    "Wannitas": 32,
    "Shuliar": 35,
    "Larba": 35,
    "Catena": 35,
    "Titore": 37,
    "Metus": 48,
    "Duplican": 48,
    "Secreta": 62,
    "Ordo": 62,
    "Asta": 62,
    "Supore": 62
}

# ======================
# 🧠 Session State Setup
# ======================
defaults = {
    "boss": "Venatus",
    "guild": "ID",
    "n": 5,
    "kill_end_date": datetime.now().date(),
    "kill_end_time": datetime.now().time(),
}

for key, value in defaults.items():
    if key not in st.session_state:
        st.session_state[key] = value

# ======================
# 🧾 Input Form
# ======================
st.subheader("⚙️ Input Data Boss")

col1, col2, col3 = st.columns(3)
with col1:
    st.session_state.boss = st.selectbox("Pilih Boss:", list(BOSS_RESPAWN.keys()), index=list(BOSS_RESPAWN.keys()).index(st.session_state.boss))
with col2:
    st.session_state.guild = st.selectbox("Guild terakhir yang kill:", ["ID", "PH"], index=["ID", "PH"].index(st.session_state.guild))
with col3:
    st.session_state.n = st.number_input("Tampilkan berapa spawn ke depan?", min_value=1, max_value=20, value=st.session_state.n, step=1)

col4, col5 = st.columns(2)
with col4:
    st.session_state.kill_end_date = st.date_input("Tanggal Kill End", st.session_state.kill_end_date)
with col5:
    st.session_state.kill_end_time = st.time_input("Waktu Kill End", st.session_state.kill_end_time)

# ======================
# 🧮 Hitung Jadwal
# ======================
kill_end_dt = datetime.combine(st.session_state.kill_end_date, st.session_state.kill_end_time)
respawn_hours = BOSS_RESPAWN[st.session_state.boss]
kill_duration = timedelta(minutes=5)
moving_time = timedelta(minutes=5)

rows = []
current_guild = st.session_state.guild
next_spawn = kill_end_dt + timedelta(hours=respawn_hours)

for i in range(st.session_state.n):
    current_guild = "PH" if current_guild == "ID" else "ID"

    spawn_time = next_spawn
    kill_start = spawn_time
    kill_end = kill_start + kill_duration
    next_spawn = kill_end + timedelta(hours=respawn_hours)

    rows.append({
        "No": i + 1,
        "Boss": st.session_state.boss,
        "Respawn (h)": respawn_hours,
        "Spawn Time (WIB)": spawn_time.strftime("%Y-%m-%d %H:%M"),
        "Kill Start (WIB)": kill_start.strftime("%Y-%m-%d %H:%M"),
        "Kill End (WIB)": kill_end.strftime("%Y-%m-%d %H:%M"),
        "Next Respawn Base": next_spawn.strftime("%Y-%m-%d %H:%M"),
        "Guild": current_guild
    })

df = pd.DataFrame(rows)

# ======================
# 📊 Output Table
# ======================
st.subheader(f"📅 Jadwal Spawn Berikutnya untuk {st.session_state.boss}")
st.dataframe(df, use_container_width=True)

# ======================
# 📘 Info Tambahan
# ======================
st.caption("""
📘 **Perhitungan Respawn:**
- Respawn dihitung dari waktu *Kill End* terakhir + durasi respawn boss.
- Kill duration dan waktu perpindahan masing-masing ±5 menit.
""")
