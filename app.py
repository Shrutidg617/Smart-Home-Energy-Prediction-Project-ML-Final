from flask import Flask, request, jsonify, render_template
import pickle
import os
from src.weather import get_weather
from database import save_record, create_table

app = Flask(__name__)

print("Starting app...")

# Create DB table
create_table()
print("Database ready")

# Load model
MODEL_PATH = os.path.join(os.path.dirname(__file__), 'models', 'model.pkl')

if not os.path.exists(MODEL_PATH):
    raise FileNotFoundError(f"model.pkl not found at {MODEL_PATH}")

with open(MODEL_PATH, 'rb') as f:
    model = pickle.load(f)

print("Model loaded")

@app.route('/')
def home():
    return render_template('index.html')


@app.route('/predict', methods=['POST'])
def predict():
    try:
        data = request.json

        hour = int(data['hour'])
        day = int(data['dayofweek'])
        month = int(data['month'])
        year = int(data['year'])

        # Weather
        temp, humidity = get_weather()

        # Prediction
        pred_value = float(model.predict([[hour, day, month, year]])[0])
        print("Prediction:", pred_value)

        # Save to DB
        save_record(hour, pred_value)

        # Suggestions
        if pred_value > 15000:
            suggestion = "High energy usage!"
            alert = "Peak usage alert!"
        elif pred_value > 10000:
            suggestion = "Moderate usage."
            alert = ""
        else:
            suggestion = "Efficient usage."
            alert = ""

        cost = pred_value * 0.12

        # ===== HOURLY GRAPH =====
        hourly_data = []
        min_energy = pred_value
        best_hour = hour

        for h in range(24):
            val = float(model.predict([[h, day, month, year]])[0])
            hourly_data.append(val)

            if val < min_energy:
                min_energy = val
                best_hour = h

        # ===== WEEKLY GRAPH =====
        weekly_data = []
        for d in range(7):
            val = float(model.predict([[hour, (day + d) % 7, month, year]])[0])
            weekly_data.append(val)

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

        # ===== SCORE =====
        score = max(0, 100 - (pred_value / 200))

        # ===== RESPONSE =====
        return jsonify({
            'prediction': pred_value,
            'suggestion': suggestion,
            'cost': cost,
            'best_hour': best_hour,
            'hourly_data': hourly_data,
            'weekly_data': weekly_data,
            'appliance_tips': appliance_tips,
            'score': score,
            'alert': alert,
            'temp': temp,
            'humidity': humidity
        })

    except Exception as e:
        print(" Error:", e)
        return jsonify({"error": str(e)})


if __name__ == "__main__":
    print("Running Flask server...")
    app.run(host="0.0.0.0", port=5000, debug=True)