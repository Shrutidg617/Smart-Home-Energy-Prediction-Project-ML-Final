# Smart Energy Prediction System

A machine learning-powered energy consumption prediction application that forecasts hourly electricity usage and provides actionable insights for energy optimization and cost savings.

## Overview

The Smart Energy Prediction System uses advanced ML models (Random Forest, XGBoost, and LSTM neural networks) to predict energy consumption patterns. It integrates with real-time weather data and provides an interactive web interface with:
- Hourly and weekly energy consumption forecasts
- Cost estimation and energy efficiency scoring
- Personalized appliance usage recommendations
- Peak usage alerts
- Historical data tracking

## Features

- **Predictive Analytics**: ML-based energy consumption forecasting
- **Real-time Weather Integration**: Weather-aware predictions
- **Interactive Dashboard**: Hour-by-hour and weekly visualization
- **Cost Calculator**: Automatic energy cost estimation
- **Energy Efficiency Scoring**: 0-100 efficiency rating system
- **Appliance Recommendations**: Optimal usage times for specific appliances
- **Database Tracking**: Save and retrieve historical predictions
- **API Endpoints**: RESTful API for prediction requests

## Project Structure

```
smart-energy-project/
├── app.py                    # Flask web application
├── database.py               # MySQL database connections
├── requirements.txt          # Python dependencies
├── Procfile                  # Heroku deployment config
│
├── src/
│   ├── lstm_model.py        # LSTM neural network training
│   ├── train.py             # Model training pipeline
│   ├── predict.py           # Prediction utilities
│   ├── preprocess.py        # Data preprocessing
│   ├── feature_engineering.py # Feature generation
│   ├── visualize.py         # Data visualization
│   └── weather.py           # Weather API integration
│
├── models/
│   ├── lstm_model.h5        # Trained LSTM model
│   └── model.pkl            # Serialized prediction model
│
├── data/
│   └── AEP_hourly.csv       # Historical hourly energy data
│
├── notebooks/
│   └── eda.ipynb            # Exploratory Data Analysis
│
├── static/
│   └── images/              # Frontend assets
│
└── templates/
    └── index.html           # Web UI
```

## Installation

### Prerequisites
- Python 3.13+
- MySQL Server
- pip or conda

### Setup

1. **Clone or download the project**
   ```bash
   cd smart-energy-project
   ```

2. **Create virtual environment**
   ```bash
   python -m venv .venv
   .venv\Scripts\Activate.ps1  # Windows
   # or
   source .venv/bin/activate  # Linux/Mac
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Configure Database**
   - Update `database.py` with your MySQL credentials:
     ```python
     mysql.connector.connect(
         host="localhost",
         user="your_username",
         password="your_password",
         database="energy_db",
         port=3306
     )
     ```
   - Create the database:
     ```bash
     mysql -u root -p < schema.sql
     ```

5. **Run the application**
   ```bash
   python app.py
   ```
   Access at `http://localhost:5000`

## Dependencies

| Package | Version | Purpose |
|---------|---------|---------|
| Flask | 3.1.3 | Web framework |
| TensorFlow/Keras | 2.18.0 | Deep learning (LSTM) |
| scikit-learn | 1.8.0 | ML algorithms (Random Forest, etc.) |
| XGBoost | 2.2.2 | Gradient boosting |
| pandas | 2.2.0 | Data manipulation |
| numpy | 2.4.3 | Numerical computing |
| matplotlib | 3.10.8 | Data visualization |
| requests | 2.33.0 | Weather API calls |
| mysql-connector-python | 9.6.0 | Database connection |

## API Endpoints

### POST `/predict`
Make energy consumption predictions.

**Request:**
```json
{
    "hour": 14,
    "dayofweek": 3,
    "month": 3,
    "year": 2024
}
```

**Response:**
```json
{
    "prediction": 12500.5,
    "suggestion": "Moderate usage.",
    "alert": "",
    "cost": 1500.06,
    "hourly_data": [...],
    "weekly_data": [...],
    "appliance_tips": [
        "Washing Machine: Use at 10:00 → Save 500 units",
        "AC: Use at 9:00 → Save 875 units"
    ],
    "efficiency_score": 92
}
```

### GET `/`
Serves the interactive web dashboard.

## Usage

1. **Open the Web Dashboard**
   - Navigate to `http://localhost:5000`
   
2. **Enter Prediction Parameters**
   - Select hour (0-23)
   - Select day of week (0-6)
   - Select month (1-12)
   - Enter year

3. **View Results**
   - Current hour prediction
   - Hours with lowest/highest usage
   - 7-day forecast
   - Estimated cost
   - Appliance usage recommendations
   - Energy efficiency score

## Data Sources

- **Historical Energy Data**: AEP hourly electricity consumption data (2004-2018)
- **Weather Data**: Real-time weather API integration
- **Features**: Hour, day of week, month, year, temperature, humidity

## Model Architecture

### LSTM Neural Network
- Input Layer: Time-series energy data
- Hidden Layers: 2 LSTM layers (50 units each) with dropout
- Output Layer: Single continuous prediction
- Optimizer: Adam
- Loss: Mean Squared Error

### Random Forest / XGBoost
- Used for tabular feature predictions
- Training on historical hourly patterns
- Feature importance analysis

## Performance Metrics

- Mean Absolute Error (MAE)
- Root Mean Square Error (RMSE)
- R² Score on validation set

## Deployment

### Local Development
```bash
python app.py
```

### Production (Gunicorn)
```bash
gunicorn -w 4 -b 0.0.0.0:5000 app:app
```

### Heroku
```bash
git push heroku main
```

## Future Enhancements

- Real-time data ingestion from smart meters
- Advanced anomaly detection
- Multi-region support
- Mobile app integration
- IoT device connectivity
- Advanced demand response automation
- User authentication and personalization

## Contributors

Developed for Smart Energy Management Systems project.

## License

MIT License - See LICENSE file for details

## Support

For issues or questions, please contact the development team.

---

**Last Updated**: March 2026
