from flask import Flask, request, jsonify, render_template
import pickle
import os
import pandas as pd
from src.weather import get_weather
from src.feature_engineering import create_features

app = Flask(__name__)

print("Starting app...")

# ===== PATHS =====
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
MODEL_PATH = os.path.join(BASE_DIR, 'models', 'model.pkl')
DATA_PATH = os.path.join(BASE_DIR, 'data', 'AEP_hourly.csv')

# ===== LOAD MODEL =====
with open(MODEL_PATH, 'rb') as f:
    model = pickle.load(f)

# ===== LOAD DATA =====
df = pd.read_csv(DATA_PATH)
df['Datetime'] = pd.to_datetime(df['Datetime'])
df = df.sort_values('Datetime').reset_index(drop=True)

print("Model + Data loaded")


@app.route('/')
def home():
    return render_template('index.html')


# ===== HELPER FUNCTION =====
def get_features_for_datetime(dt):
    df['time_diff'] = abs(df['Datetime'] - dt)
    row = df.loc[df['time_diff'].idxmin()]
    idx = row.name

    # Lag features
    lag_1 = df.iloc[idx - 1]['AEP_MW'] if idx > 0 else row['AEP_MW']
    lag_24 = df.iloc[idx - 24]['AEP_MW'] if idx >= 24 else lag_1
    rolling_mean_24 = df.iloc[max(0, idx-24):idx]['AEP_MW'].mean()

    temp_df = pd.DataFrame({'Datetime': [dt]})
    temp_df = create_features(temp_df)

    features = temp_df.drop(columns=['Datetime'])

    features['lag_1'] = lag_1
    features['lag_24'] = lag_24
    features['rolling_mean_24'] = rolling_mean_24

    # Exact feature order (VERY IMPORTANT)
    features = features[['hour', 'dayofweek', 'month', 'year', 'is_weekend',
                         'lag_1', 'lag_24', 'rolling_mean_24']]

    return features


@app.route('/predict', methods=['POST'])
def predict():
    try:
        data = request.json

        hour = int(data['hour'])
        date = int(data['date'])
        month = int(data['month'])
        year = int(data['year'])

        # Weather
        temp, humidity = get_weather()

        # Input datetime
        input_datetime = pd.to_datetime(
            f"{year}-{month:02d}-{date:02d} {hour:02d}:00:00"
        )

        # ===== MAIN PREDICTION =====
        features = get_features_for_datetime(input_datetime)
        pred_value = float(model.predict(features)[0])

        # ===== HOURLY GRAPH =====
        hourly_data = []
        min_energy = pred_value
        best_hour = hour

        for h in range(24):
            dt = input_datetime.replace(hour=h)
            f = get_features_for_datetime(dt)
            val = float(model.predict(f)[0])
            hourly_data.append(val)

            if val < min_energy:
                min_energy = val
                best_hour = h

        # ===== WEEKLY GRAPH =====
        weekly_data = []
        for d in range(7):
            dt = input_datetime + pd.Timedelta(days=d)
            f = get_features_for_datetime(dt)
            val = float(model.predict(f)[0])
            weekly_data.append(val)

        # ===== COST =====
        cost = pred_value * 0.12

        # ===== SCORE =====
        score = max(0, 100 - (pred_value / 200))

        # ===== ALERT =====
        if pred_value > 15000:
            alert = "⚠️ Peak usage alert!"
        elif pred_value > 12000:
            alert = "Moderate usage"
        else:
            alert = "Efficient usage"

        # ===== APPLIANCE TIPS =====
        appliances = {
            "Washing Machine": 2.0,
            "AC": 3.5,
            "Heater": 4.0
        }

        appliance_tips = []
        for name, power in appliances.items():
            savings = (pred_value - min_energy) * power
            appliance_tips.append(
                f"{name}: Use at {best_hour}:00 → Save {savings:.2f} units"
            )

        return jsonify({
            'prediction': pred_value,
            'cost': cost,
            'score': score,
            'alert': alert,
            'appliance_tips': appliance_tips,
            'hourly_data': hourly_data,
            'weekly_data': weekly_data,
            'best_hour': best_hour,
            'temp': temp,
            'humidity': humidity
        })

    except Exception as e:
        print("Error:", e)
        return jsonify({"error": str(e)})


if __name__ == "__main__":
    app.run(debug=True)