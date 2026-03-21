import numpy as np
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import LSTM, Dense

def create_dataset(data, time_step=10):
    X, y = [], []
    for i in range(len(data)-time_step):
        X.append(data[i:(i+time_step)])
        y.append(data[i+time_step])
    return np.array(X), np.array(y)

def train_lstm(series):
    series = series.values.reshape(-1,1)

    X, y = create_dataset(series)

    model = Sequential([
        LSTM(50, return_sequences=True, input_shape=(X.shape[1],1)),
        LSTM(50),
        Dense(1)
    ])

    model.compile(optimizer='adam', loss='mse')
    model.fit(X, y, epochs=5, batch_size=32)

    return model