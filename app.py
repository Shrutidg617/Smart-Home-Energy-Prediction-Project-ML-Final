from flask import Flask, request, jsonify, render_template
import pickle, os
from src.weather import get_weather
from database import save_record

app = Flask(__name__)

model = pickle.load(open('models/model.pkl', 'rb'))

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/predict', methods=['POST'])
def predict():
    data = request.json

    hour = int(data['hour'])
    day = int(data['dayofweek'])
    month = int(data['month'])
    year = int(data['year'])

    # 🌦️ Weather
    temp, humidity = get_weather()

    # Prediction
    pred_value = float(model.predict([[hour, day, month, year]])[0])

    # Save to DB
    save_record(hour, pred_value)

    # Suggestion
    if pred_value > 15000:
        suggestion = "⚠️ High energy usage!"
        alert = "⚠️ Peak usage alert!"
    elif pred_value > 10000:
        suggestion = "Moderate usage."
        alert = ""
    else:
        suggestion = "Efficient usage."
        alert = ""

    cost = pred_value * 0.12

    # 📊 24-hour graph
    hourly_data = []
    min_energy = pred_value
    best_hour = hour

    for h in range(24):
        val = float(model.predict([[h, day, month, year]])[0])
        hourly_data.append(val)

        if val < min_energy:
            min_energy = val
            best_hour = h

    # 📅 Weekly forecast
    weekly_data = []
    for d in range(7):
        val = float(model.predict([[hour, (day+d)%7, month, year]])[0])
        weekly_data.append(val)

    # 🧠 Appliance Scheduler
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

    # 📉 Efficiency score
    score = max(0, 100 - (pred_value / 200))

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

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)