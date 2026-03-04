import pandas as pd
import joblib
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report, accuracy_score

# ===============================
# 1️⃣ Load Dataset
# ===============================

print("Loading dataset...")
df = pd.read_csv("dataset/disease_symptoms.csv")

# Remove unwanted column if exists
if "Unnamed: 133" in df.columns:
    df = df.drop("Unnamed: 133", axis=1)

print("Dataset shape:", df.shape)

# ===============================
# 2️⃣ Features & Labels
# ===============================

X = df.drop("prognosis", axis=1)
y = df["prognosis"]

print("Total symptoms:", len(X.columns))
print("Total diseases:", len(y.unique()))

# ===============================
# 3️⃣ Train Test Split
# ===============================

X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42
)

print("Training samples:", X_train.shape[0])
print("Testing samples:", X_test.shape[0])

# ===============================
# 4️⃣ Train RandomForest Model
# ===============================

print("\nTraining RandomForest model...")

model = RandomForestClassifier(
    n_estimators=300,
    random_state=42,
    n_jobs=-1
)

model.fit(X_train, y_train)

# ===============================
# 5️⃣ Evaluation
# ===============================

print("\nEvaluating model...")

y_pred = model.predict(X_test)

accuracy = accuracy_score(y_test, y_pred)

print("\nAccuracy:", round(accuracy * 100, 2), "%")
print("\nClassification Report:\n")
print(classification_report(y_test, y_pred))

# ===============================
# 6️⃣ Save Model & Columns
# ===============================

print("\nSaving model...")

import os
os.makedirs("backend/ml_models", exist_ok=True)
joblib.dump(model, "backend/ml_models/model.pkl")
joblib.dump(X.columns.tolist(), "backend/ml_models/symptom_columns.pkl")

print("\nModel trained and saved successfully!")
print("Saved files:")
print(" - backend/ml_models/model.pkl")
print(" - backend/ml_models/symptom_columns.pkl")