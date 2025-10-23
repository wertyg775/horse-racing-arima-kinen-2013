import pandas as pd
import sqlite3
import os

# Paths
data_path = r"C:\Users\User\Documents\horse-racing-arima-kinen-2013\data\processed\cleaned.xlsx"
db_path = r"C:\Users\User\Documents\horse-racing-arima-kinen-2013\data\races.db"

# Create DB folder if not exists
os.makedirs(os.path.dirname(db_path), exist_ok=True)

# Load your race data
df = pd.read_excel(data_path)

# Create SQLite database and write table
conn = sqlite3.connect(db_path)
df.to_sql("race_history", conn, if_exists="replace", index=False)
conn.close()

print("✅ Database setup complete! Saved to:", db_path)
