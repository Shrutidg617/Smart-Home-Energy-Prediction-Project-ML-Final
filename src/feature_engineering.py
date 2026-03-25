import pandas as pd

def create_features(df):
    df['hour'] = df['Datetime'].dt.hour
    df['dayofweek'] = df['Datetime'].dt.dayofweek
    df['month'] = df['Datetime'].dt.month
    df['year'] = df['Datetime'].dt.year  

    # lag features
    df['lag1'] = df['AEP_MW'].shift(1)
    df['lag2'] = df['AEP_MW'].shift(2)

    # rolling features
    df['rolling_mean_3'] = df['AEP_MW'].rolling(window=3).mean()

    df = df.dropna()
    return df