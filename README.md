# 🏇 Horse Racing Win Probability Prediction — Arima Kinen 2013

## 📘 Overview
This project predicts the **winning probability of each horse** in the **Arima Kinen 2013** race using historical race data from **Netkeiba**.
The approach treats each horse’s past race record as a training example for a **Random Forest binary classification model**, predicting whether the horse will **win (1)** or **not win (0)**.
The probabilities from the classifier are then **aggregated across horses** in the same race to estimate their relative chances of winning.

---

## 🧭 Project Workflow

### 1. Data Collection
- Historical race data was scraped from **Netkeiba**, containing:
  - Race details (date, distance, surface, weather, etc.)
  - Horse information (age, sex, race history, popularity)
  - Jockey and trainer details
  - Finishing position and odds  

### 2. Data Cleaning
- Removed duplicates and handled missing values using `SimpleImputer`.
- Standardized column names and data types.
- Filtered records to include only relevant races leading up to **Arima Kinen 2013**.

### 3. Feature Engineering
- Created aggregated horse-level performance statistics:
  - Average finish position
  - Historical win rates
  - Race distance and surface history  
- Applied **one-hot encoding** for categorical variables using `ColumnTransformer`.
- Combined preprocessing and modeling using a `Pipeline`.

### 4. Modeling
- **Algorithm:** `RandomForestClassifier` from scikit-learn.  
- **Target:** Binary (1 = Win, 0 = Not Win).  
- The model outputs a **probability of winning** for each horse.  
- Final probabilities are **normalized within each race** to compare horses fairly.

### 5. Evaluation
- Model performance assessed using:
  - **ROC-AUC Score**
  - **Accuracy**
  - **Classification Report (Precision, Recall, F1)**  

### 6. Model Saving
- Final trained model saved using **joblib** for future predictions:
  ```python
  import joblib
  joblib.dump(model, "models/rf_model.pkl")
  ```

### 7. Streamlit Integration
- A Streamlit interface is being developed for:
  - Displaying predicted probabilities
  - Ranking horses by win likelihood
  - Visualizing model performance

---

## 📂 Project Structure
```
horse-racing-arima-kinen-2013/
│
├── data/
│   ├── raw/                # Scraped Netkeiba data
│   ├── cleaned/            # Processed datasets
│
├── models/
│   └── rf_model.pkl        # Trained Random Forest model
│
├── notebooks/
│   └── modelling.ipynb     # Model training and evaluation
│
├── src/
│   ├── scraping.py
│   ├── preprocessing.py
│   ├── feature_engineering.py
│   └── predict.py
│
└── README.md
```

---

## ⚙️ Dependencies
```
scikit-learn
numpy
pandas
matplotlib
scipy
streamlit
joblib
```

All required libraries can be installed via:
```bash
pip install -r requirements.txt
```

---

## 🚀 Summary
This project demonstrates how machine learning can be applied to horse racing prediction.
By combining **historical data**, **feature engineering**, and a **Random Forest binary classifier**, the model estimates realistic **winning probabilities** for each horse in the **Arima Kinen 2013** race.
