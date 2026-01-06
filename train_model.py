import pandas as pd
import joblib
from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import train_test_split
import os

# Load the updated dataset
df = pd.read_csv("life_expectancy_preprocessed_with_target.csv")

# Drop non-numeric / non-feature columns
X = df.drop(columns=["Country", "Status", "Life expectancy"])
y = df["Life expectancy"]

# Train model
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42
)

model = RandomForestRegressor(n_estimators=200, random_state=42)
model.fit(X_train, y_train)

# Save model + feature names
os.makedirs("model", exist_ok=True)
joblib.dump(model, "model/model.pkl")
joblib.dump(list(X_train.columns), "model/features.pkl")  # ⭐ NEW LINE

print("Feature count:", X_train.shape[1])
print("Model trained and saved successfully.")


