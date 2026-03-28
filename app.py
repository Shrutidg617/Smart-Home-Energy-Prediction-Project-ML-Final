# from flask import Flask, request, jsonify, render_template
# import pickle, os
# from src.weather import get_weather
# from database import save_record, create_table

# app = Flask(__name__)

# # ✅ Load model
# model = pickle.load(open('models/model.pkl', 'rb'))

# # ✅ CREATE TABLE HERE (IMPORTANT FIX)
# create_table()

# @app.route('/')
# def home():
#     return render_template('index.html')
# # @app.route('/')
# # def home():
# #     return "HOME WORKING"

# @app.route('/predict', methods=['POST'])
# def predict():
#     data = request.json

#     hour = int(data['hour'])
#     day = int(data['dayofweek'])
#     month = int(data['month'])
#     year = int(data['year'])

#     temp, humidity = get_weather()

#     pred_value = float(model.predict([[hour, day, month, year]])[0])

#     save_record(hour, pred_value)

#     if pred_value > 15000:
#         suggestion = "⚠️ High energy usage!"
#         alert = "⚠️ Peak usage alert!"
#     elif pred_value > 10000:
#         suggestion = "Moderate usage."
#         alert = ""
#     else:
#         suggestion = "Efficient usage."
#         alert = ""

#     cost = pred_value * 0.12

#     hourly_data = []
#     min_energy = pred_value
#     best_hour = hour

#     for h in range(24):
#         val = float(model.predict([[h, day, month, year]])[0])
#         hourly_data.append(val)

#         if val < min_energy:
#             min_energy = val
#             best_hour = h

#     weekly_data = []
#     for d in range(7):
#         val = float(model.predict([[hour, (day+d)%7, month, year]])[0])
#         weekly_data.append(val)

#     appliances = {
#         "Washing Machine": 2.0,
#         "AC": 3.5,
#         "Heater": 4.0
#     }

#     appliance_tips = []
#     for name, power in appliances.items():
#         savings = (pred_value - min_energy) * power
#         appliance_tips.append(
#             f"{name}: Use at {best_hour}:00 → Save {savings:.2f} units"
#         )

#     score = max(0, 100 - (pred_value / 200))

#     return jsonify({
#         'prediction': pred_value,
#         'suggestion': suggestion,
#         'cost': cost,
#         'best_hour': best_hour,
#         'hourly_data': hourly_data,
#         'weekly_data': weekly_data,
#         'appliance_tips': appliance_tips,
#         'score': score,
#         'alert': alert,
#         'temp': temp,
#         'humidity': humidity
#     })

# # ✅ KEEP THIS ONLY FOR LOCAL RUN (Railway ignores it)
# if __name__ == "__main__":
#     app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 10000)))

from flask import Flask, request, jsonify, render_template
import pickle
import os
from src.weather import get_weather
from database import save_record, create_table

app = Flask(__name__)

# Create DB table
create_table()

# Load model safely
MODEL_PATH = os.path.join(os.path.dirname(__file__), 'models', 'model.pkl')
if not os.path.exists(MODEL_PATH):
    raise FileNotFoundError(
        f"❌ model.pkl not found at {MODEL_PATH}. "
        "Please run train.py locally and commit models/model.pkl to your repo."
    )
model = pickle.load(open(MODEL_PATH, 'rb'))
print("✅ Model loaded successfully")

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

    temp, humidity = get_weather()
    pred_value = float(model.predict([[hour, day, month, year]])[0])
    save_record(hour, pred_value)

    if pred_value > 15000:
        suggestion = "⚠️ High energy usage!"
        alert = "🚨 Peak usage alert!"
    elif pred_value > 10000:
        suggestion = "Moderate usage."
        alert = ""
    else:
        suggestion = "✅ Efficient usage."
        alert = ""

    cost = pred_value * 0.12

    hourly_data = []
    min_energy = pred_value
    best_hour = hour
    for h in range(24):
        val = float(model.predict([[h, day, month, year]])[0])
        hourly_data.append(val)
        if val < min_energy:
            min_energy = val
            best_hour = h

    weekly_data = []
    for d in range(7):
        val = float(model.predict([[hour, (day + d) % 7, month, year]])[0])
        weekly_data.append(val)

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
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 10000)))