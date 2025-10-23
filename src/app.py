import streamlit as st
import pandas as pd
import joblib
import sqlite3
import os


# ===========================================================
# 🧠 Load model + features safely
# ===========================================================
BASE_DIR = os.path.dirname(os.path.dirname(__file__))  # one level above /src

# --- Model ---
MODEL_PATH = os.path.join(BASE_DIR, "models", "arima_model.pkl")
if not os.path.exists(MODEL_PATH):
    st.error(f"❌ Model file not found at: {MODEL_PATH}")
else:
    model = joblib.load(MODEL_PATH)

# --- Features ---
FEATURES_PATH = os.path.join(BASE_DIR, "data", "processed", "arima_kinen_features.csv")
if not os.path.exists(FEATURES_PATH):
    st.error(f"❌ Feature file not found at: {FEATURES_PATH}")
    st.stop()
else:
    features = pd.read_csv(FEATURES_PATH)

# --- Database ---
DB_PATH = os.path.join(BASE_DIR, "data", "races.db")
if not os.path.exists(DB_PATH):
    st.warning(f"⚠️ Race history database not found at: {DB_PATH}")


def get_asset_path(filename):
    """Safely get the absolute path for assets within the /src/assets folder."""
    base_dir = os.path.dirname(__file__)
    return os.path.join(base_dir, "assets", filename)


feature_cols = [
    'Speed_kph', 'PosChange', 'FinalCornerPos', 'Runners',
    'AvgPlacement_Last3', 'DaysSinceLastRace', 'Distance',
    'RaceGrade_numeric', 'Course', 'Track'
]

# ===========================================================
# 🏇 Page Title
# ===========================================================
st.image(get_asset_path("banner.jpg"), use_container_width=True)
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
    "Orfevre": get_asset_path("Orfevre.jpg"),
    "Gold Ship": get_asset_path("Gold_Ship.jpg"),
    "Win Variation": get_asset_path("Win_Variation.jpg"),
    "Love Is Boo Shet": get_asset_path("Love_Is_Boo_Shet.jpg"),
    "Tamamo Best Play": get_asset_path("Tamamo_Best_Play.jpg"),
    "Curren Mirotic": get_asset_path("Curren_Mirotic.jpg"),
    "Desperado": get_asset_path("Desperado.jpg"),
    "To The Glory": get_asset_path("To_The_Glory.jpg"),
    "T M Inazuma": get_asset_path("TM_Inazuma.jpg"),
    "Verde Green": get_asset_path("Verde_Green.jpg"),
    "Admire Rakti": get_asset_path("Admire_Rakti.jpg"),
    "Lovely Day": get_asset_path("Lovely_Day.jpg"),
    "Nakayama Knight": get_asset_path("Nakayama_Knight.jpg"),
    "Tosen Jordan": get_asset_path("Tosen_Jordan.jpg"),
    "Danon Ballade": get_asset_path("Danon_Ballade.jpg"),
    "Lelouch": get_asset_path("Lelouch.jpg"),
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
