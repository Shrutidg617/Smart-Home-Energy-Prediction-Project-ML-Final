import pandas as pd
import pickle
import os
from xgboost import XGBRegressor
from src.preprocess import load_and_process

print("Training model...")

# Load dataset
df = load_and_process("data/AEP_hourly.csv")

# Features & Target
X = df.drop(columns=['AEP_MW', 'Datetime'])
y = df['AEP_MW']

# Train model
model = XGBRegressor(n_estimators=100, learning_rate=0.1)
model.fit(X, y)

# Save model
os.makedirs("models", exist_ok=True)
with open("models/model.pkl", "wb") as f:
    pickle.dump(model, f)

print("Model trained and saved!")




