import streamlit as st
import pickle

model = pickle.load(open('models/model.pkl', 'rb'))

st.title("⚡ Energy Consumption Predictor")

hour = st.number_input("Hour", 0, 23)
day = st.number_input("Day of Week (0=Mon)", 0, 6)
month = st.number_input("Month", 1, 12)
year = st.number_input("Year", 2000, 2030)

if st.button("Predict"):
    prediction = model.predict([[hour, day, month, year]])
    st.success(f"Predicted Energy: {prediction[0]:.2f}")