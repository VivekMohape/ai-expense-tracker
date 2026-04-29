import pandas as pd

def clean_data(df):
    df.columns = df.columns.str.strip()

    df['WITHDRAWAL AMT'] = pd.to_numeric(df['WITHDRAWAL AMT'], errors='coerce').fillna(0)
    df['DEPOSIT AMT'] = pd.to_numeric(df['DEPOSIT AMT'], errors='coerce').fillna(0)

    # Normalize amount
    df['amount'] = df['DEPOSIT AMT'] - df['WITHDRAWAL AMT']

    df = df.rename(columns={
        "DATE": "date",
        "TRANSACTION DETAILS": "description",
        "BALANCE AMT": "balance"
    })

    df = df[['date', 'description', 'amount', 'balance']]

    # Remove empty descriptions
    df = df[df['description'].notna()]

    return df
