import pandas as pd
import numpy as np
from sklearn.linear_model import LinearRegression

def prepare_monthly_data(df):
    df = df.copy()

    df_exp = df[df['amount'] < 0].copy()

    df_exp['month'] = df_exp['date'].dt.to_period('M')

    monthly = df_exp.groupby('month')['amount'].sum().reset_index()

    monthly['month_index'] = np.arange(len(monthly))

    return monthly


def train_model(monthly):
    X = monthly[['month_index']]
    y = monthly['amount']

    model = LinearRegression()
    model.fit(X, y)

    return model


def predict_next_month(model, monthly):
    next_idx = monthly['month_index'].max() + 1
    pred = model.predict([[next_idx]])

    return float(pred[0])
