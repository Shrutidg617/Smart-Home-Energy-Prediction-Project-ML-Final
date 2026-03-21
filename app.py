from flask import Flask, request, jsonify, render_template
import pickle
app = Flask(__name__)

model = pickle.load(open('models/model.pkl', 'rb'))

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/predict', methods=['POST'])
def predict():
    data = request.json

    features = [[
        int(data['hour']),
        int(data['dayofweek']),
        int(data['month']),
        int(data['year'])
    ]]

    prediction = model.predict(features)
    # if prediction[0] > 15000:
    #     suggestion = "High energy usage! Try reducing appliances during peak hours."
    # elif prediction[0] > 10000:
    #     suggestion = "Moderate usage. Consider optimizing usage timing."
    # else:
    #     suggestion = " Energy usage is efficient."

    # optimization Logic
    pred_value = float(prediction[0])

    if pred_value > 15000:
        suggestion = "High energy usage! Try reducing appliances during peak hours."
    elif pred_value > 10000:
        suggestion = "Moderate usage. Consider optimizing usage timing."
    else:
        suggestion = "Energy usage is efficient."

    # Cost estimation (example rate)
    cost = pred_value * 0.12

    return jsonify({
        'prediction': pred_value,
        'suggestion': suggestion,
        'cost': cost
})

if __name__ == "__main__":
    # app.run(debug=True)
    app.run(host="0.0.0.0", port=10000)