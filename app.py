import streamlit as st
import pandas as pd
import plotly.express as px

from preprocess import clean_data
from llm_classifier import classify_transaction
from db import init_db, save_data
from model import prepare_monthly_data, train_model, predict_next_month

st.set_page_config(layout="wide")
st.title(" AI Expense Dashboard")

uploaded = st.file_uploader("Upload Bank CSV/Excel", type=["csv", "xlsx"])

if uploaded:

    #  Load file
    if uploaded.name.endswith(".xlsx"):
        df = pd.read_excel(uploaded)
    else:
        df = pd.read_csv(uploaded)

    df = clean_data(df)

    st.subheader(" Cleaned Data")
    st.dataframe(df.head())

    #  Caching classification
    @st.cache_data
    def classify_cached(desc):
        return classify_transaction(desc)

    st.subheader(" Classifying Transactions...")
    df['category'] = df['description'].apply(classify_cached)

    st.success("Classification Done")

    #  Save
    init_db()
    save_data(df)

    #  Expense only
    df_exp = df[df['amount'] < 0].copy()
    df_exp['amount'] = df_exp['amount'].abs()

    # PIE
    st.subheader(" Category Distribution")
    fig1 = px.pie(df_exp, names="category", values="amount")
    st.plotly_chart(fig1, use_container_width=True)

    #  Monthly
    monthly = prepare_monthly_data(df)

    model = train_model(monthly)
    pred = predict_next_month(model, monthly)

    monthly['month'] = monthly['month'].astype(str)

    st.subheader(" Monthly Expense Trend")

    fig2 = px.line(monthly, x="month", y="amount", markers=True)

    fig2.add_scatter(
        x=[monthly['month'].iloc[-1], "Next Month"],
        y=[monthly['amount'].iloc[-1], pred],
        mode='lines+markers',
        line=dict(dash='dot'),
        name="Prediction"
    )

    st.plotly_chart(fig2, use_container_width=True)

    st.metric("📉 Predicted Expense (Next Month)", f"{abs(pred):.2f}")
