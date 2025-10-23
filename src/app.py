import streamlit as st
import pandas as pd
import joblib
import sqlite3
import os


# ===========================================================
# 🧠 Load model + features
# ===========================================================
MODEL_PATH = r"C:\Users\User\Documents\horse-racing-arima-kinen-2013\models\arima_model.pkl"
FEATURES_PATH = r"C:\Users\User\Documents\horse-racing-arima-kinen-2013\data\processed\arima_kinen_features.csv"
DB_PATH = r"C:\Users\User\Documents\horse-racing-arima-kinen-2013\data\races.db"

model = joblib.load(MODEL_PATH)
features = pd.read_csv(FEATURES_PATH)

feature_cols = [
    'Speed_kph', 'PosChange', 'FinalCornerPos', 'Runners',
    'AvgPlacement_Last3', 'DaysSinceLastRace', 'Distance',
    'RaceGrade_numeric', 'Course', 'Track'
]

# ===========================================================
# 🏇 Page Title
# ===========================================================
st.image("assets/banner.jpg", use_container_width=True)
st.title("🏆 Arima Kinen 2013 — Prediction Dashboard")
st.markdown("""
Welcome to the **Arima Kinen 2013 Race Predictor**!  
Explore model predictions and interactively view race history or model details using the sidebar pages.
""")

st.video("https://youtu.be/jXHtadsETOk?si=bgndxwv29AhgtXGC")

# ===========================================================
# 🎛️ Sidebar — Race Settings
# ===========================================================
st.sidebar.header("🧩 Adjust Race Parameters")

distance = st.sidebar.slider("Race Distance (m)", 1800, 3200, 2500, step=100)
grade_label = st.sidebar.selectbox("Race Grade", ["G1", "G2", "G3"])
grade_map = {"G1": 3, "G2": 2, "G3": 1}
grade = grade_map[grade_label]
course = st.sidebar.selectbox("Racecourse", ["NAK", "TOK", "KYO", "HAN"])
track = st.sidebar.selectbox("Surface", ["Turf", "Dirt"])

# Apply context
features["Distance"] = distance
features["RaceGrade_numeric"] = grade
features["Course"] = course
features["Track"] = track
features["Runners"] = 16

# ===========================================================
# 🧮 Model Prediction
# ===========================================================
features["Win_Prob"] = model.predict_proba(features[feature_cols])[:, 1]
features["Win_Prob_Normalized"] = features["Win_Prob"] / features["Win_Prob"].sum()
leaderboard = features[["Horse", "Win_Prob_Normalized"]].sort_values(
    "Win_Prob_Normalized", ascending=False).reset_index(drop=True)
leaderboard["Win_Prob_%"] = (leaderboard["Win_Prob_Normalized"] * 100).round(2)

# ===========================================================
# 🏁 Interactive Leaderboard
# ===========================================================
st.subheader("🏇 Predicted Win Probabilities")

horse_images = {
    "Orfevre": r"C:\Users\User\Documents\horse-racing-arima-kinen-2013\src\assets\Orfevre.jpg",
    "Gold Ship": r"C:\Users\User\Documents\horse-racing-arima-kinen-2013\src\assets\Gold_Ship.jpg",
    "Win Variation": r"C:\Users\User\Documents\horse-racing-arima-kinen-2013\src\assets\Win_Variation.jpg",
    "Love Is Boo Shet": r"C:\Users\User\Documents\horse-racing-arima-kinen-2013\src\assets\Love_Is_Boo_Shet.jpg",
    "Tamamo Best Play": r"C:\Users\User\Documents\horse-racing-arima-kinen-2013\src\assets\Tamamo_Best_Play.jpg",
    "Curren Mirotic": r"C:\Users\User\Documents\horse-racing-arima-kinen-2013\src\assets\Curren_Mirotic.jpg",
    "Desperado": r"C:\Users\User\Documents\horse-racing-arima-kinen-2013\src\assets\Desperado.jpg",
    "To The Glory": r"C:\Users\User\Documents\horse-racing-arima-kinen-2013\src\assets\To_The_Glory.jpg",
    "T M Inazuma": r"C:\Users\User\Documents\horse-racing-arima-kinen-2013\src\assets\TM_Inazuma.jpg",
    "Verde Green": r"C:\Users\User\Documents\horse-racing-arima-kinen-2013\src\assets\Verde_Green.jpg",
    "Admire Rakti": r"C:\Users\User\Documents\horse-racing-arima-kinen-2013\src\assets\Admire_Rakti.jpg",
    "Lovely Day": r"C:\Users\User\Documents\horse-racing-arima-kinen-2013\src\assets\Lovely_Day.jpg",
    "Nakayama Knight": r"C:\Users\User\Documents\horse-racing-arima-kinen-2013\src\assets\Nakayama_Knight.jpg",
    "Tosen Jordan": r"C:\Users\User\Documents\horse-racing-arima-kinen-2013\src\assets\Tosen_Jordan.jpg",
    "Danon Ballade": r"C:\Users\User\Documents\horse-racing-arima-kinen-2013\src\assets\Danon_Ballade.jpg",
    "Lelouch": r"C:\Users\User\Documents\horse-racing-arima-kinen-2013\src\assets\Lelouch.jpg",
}

# ===========================================================
# 🏁 Display Leaderboard (Static)
# ===========================================================

for _, row in leaderboard.iterrows():
    cols = st.columns([1, 3, 2])
    with cols[0]:
        image_path = horse_images.get(row["Horse"])
        if image_path and os.path.exists(image_path):
            st.image(image_path, width=80)
    with cols[1]:
        st.markdown(f"**{row['Horse']}**")
    with cols[2]:
        st.markdown(f"**{row['Win_Prob_%']}% chance**")

st.bar_chart(data=leaderboard, x="Horse", y="Win_Prob_%", use_container_width=True)


# ===========================================================
# 📋 Race History Viewer (Dropdown version)
# ===========================================================
st.markdown("---")
st.subheader("📜 Race History Viewer")

# Connect to SQLite database
conn = sqlite3.connect(DB_PATH)

# Dropdown to select horse
selected_horse = st.selectbox(
    "Select a horse to view race history:",
    leaderboard["Horse"].tolist()
)

# Columns you want to show in history
columns_to_show = ["Race", "RaceGrade", "Finish", "Runners"]

# Query horse's race history
query = f"""
SELECT {', '.join(columns_to_show)}
FROM race_history
WHERE Horse = ?
ORDER BY RaceDate DESC;
"""
horse_history = pd.read_sql_query(query, conn, params=(selected_horse,))
conn.close()

# Display horse image (if available)
if selected_horse in horse_images and os.path.exists(horse_images[selected_horse]):
    st.image(horse_images[selected_horse], width=150)

# Display the history table
st.write(f"### 🐎 Race History for **{selected_horse}**")
st.dataframe(horse_history, use_container_width=True)

# Basic summary statistics
if not horse_history.empty:
    st.markdown(f"**Total Races:** {len(horse_history)}")
    st.markdown(f"**Average Finish:** {horse_history['Finish'].mean():.2f}")
else:
    st.warning("No race history found for this horse.")

# Footer
st.markdown("""
---
👤 *Built by [Muhammad Danish Luqman bin Shaifuddin]*  
📊 Predicting the 2013 Arima Kinen using machine learning.
""")
