import pandas as pd

def clean_data(df):
    df.columns = df.columns.str.strip()

    # Drop unwanted column
    if '.' in df.columns:
        df = df.drop(columns=['.'])

    df['WITHDRAWAL AMT'] = pd.to_numeric(df['WITHDRAWAL AMT'], errors='coerce').fillna(0)
    df['DEPOSIT AMT'] = pd.to_numeric(df['DEPOSIT AMT'], errors='coerce').fillna(0)
    df['BALANCE AMT'] = pd.to_numeric(df['BALANCE AMT'], errors='coerce')

    df['amount'] = df['DEPOSIT AMT'] - df['WITHDRAWAL AMT']

    df = df.rename(columns={
        "DATE": "date",
        "TRANSACTION DETAILS": "description",
        "BALANCE AMT": "balance"
    })

    df['date'] = pd.to_datetime(df['date'], errors='coerce')

    df = df[['date', 'description', 'amount', 'balance']]
    df = df.dropna(subset=['description', 'date'])

    return df
