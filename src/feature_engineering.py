def create_features(df):
    df['hour'] = df['Datetime'].dt.hour
    df['dayofweek'] = df['Datetime'].dt.dayofweek
    df['month'] = df['Datetime'].dt.month
    df['year'] = df['Datetime'].dt.year
    df['is_weekend'] = df['dayofweek'].isin([5, 6]).astype(int)

    # Only create lag features if AEP_MW exists (training time)
    if 'AEP_MW' in df.columns:
        df['lag_1'] = df['AEP_MW'].shift(1)
        df['lag_24'] = df['AEP_MW'].shift(24)
        df['rolling_mean_24'] = df['AEP_MW'].rolling(24).mean()

    df = df.fillna(0)
    return df