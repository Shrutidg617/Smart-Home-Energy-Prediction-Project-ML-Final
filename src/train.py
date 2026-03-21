import pickle
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_absolute_error
from preprocess import load_and_process
from xgboost import XGBRegressor
import os

# Load data
df = load_and_process('data/AEP_hourly.csv')

# Features and target
# X = df[['hour', 'dayofweek', 'month', 'year']]
X = df[['hour', 'dayofweek', 'month', 'year', 'lag1', 'lag2', 'rolling_mean_3']]
y = df['AEP_MW']

# Split (IMPORTANT: shuffle=False for time series)
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, shuffle=False
)

# Train RandomForest model
rf_model = RandomForestRegressor(n_estimators=100)
rf_model.fit(X_train, y_train)

# Save model (ensure path is correct)
model_path = os.path.join(os.path.dirname(__file__), '..', 'models', 'model.pkl')
pickle.dump(rf_model, open(model_path, 'wb'))

print("RandomForest model trained and saved!")

# Evaluate RandomForest
rf_preds = rf_model.predict(X_test)
rf_mae = mean_absolute_error(y_test, rf_preds)
print("RandomForest MAE:", rf_mae)

# Train XGBoost model
xgb_model = XGBRegressor(n_estimators=200, learning_rate=0.05)
xgb_model.fit(X_train, y_train)

# Evaluate XGBoost
xgb_preds = xgb_model.predict(X_test)
xgb_mae = mean_absolute_error(y_test, xgb_preds)
print("XGBoost MAE:", xgb_mae)

if xgb_mae < rf_mae:
    best_model = xgb_model
else:
    best_model = rf_model

pickle.dump(best_model, open(model_path, 'wb'))