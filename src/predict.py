import pickle

# model = pickle.load(open('../models/model.pkl', 'rb'))
import os

model_path = os.path.join(os.path.dirname(__file__), '..', 'models', 'model.pkl')
model = pickle.load(open(model_path, 'rb'))

def predict(hour, dayofweek, month, year):
    return model.predict([[hour, dayofweek, month, year]])