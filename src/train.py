import pickle
import os
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_absolute_error
from src.preprocess import load_and_process
from xgboost import XGBRegressor

# Ensure models folder exists
os.makedirs('models', exist_ok=True)

# Load data
df = load_and_process('data/AEP_hourly.csv')

# Features
X = df[['hour', 'dayofweek', 'month', 'year']]
y = df['AEP_MW']

# Split
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, shuffle=False
)

# Train RF
rf_model = RandomForestRegressor(n_estimators=100)
rf_model.fit(X_train, y_train)

rf_preds = rf_model.predict(X_test)
rf_mae = mean_absolute_error(y_test, rf_preds)

# Train XGB
xgb_model = XGBRegressor(n_estimators=200, learning_rate=0.05)
xgb_model.fit(X_train, y_train)

xgb_preds = xgb_model.predict(X_test)
xgb_mae = mean_absolute_error(y_test, xgb_preds)

print("RF MAE:", rf_mae)
print("XGB MAE:", xgb_mae)

# Save best
best_model = xgb_model if xgb_mae < rf_mae else rf_model

pickle.dump(best_model, open('models/model.pkl', 'wb'))

print("Best model saved!")