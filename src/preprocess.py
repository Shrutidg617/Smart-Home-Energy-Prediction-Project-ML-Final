import pandas as pd

from feature_engineering import create_features

def load_and_process(path):
    df = pd.read_csv(path, parse_dates=['Datetime'])
    df = df.sort_values('Datetime')

    df = create_features(df)

    return df