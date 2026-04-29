import streamlit as st
import pandas as pd
import plotly.express as px

from preprocess import clean_data
from llm_classifier import classify_transaction
from db import init_db, save_data
from model import prepare_monthly_data, train_model, predict_next_month

st.set_page_config(layout="wide")
st.title("AI Expense Dashboard")

# Data Source Selection
data_source = st.radio(
    "Select Data Source",
    ["Upload File", "Use Demo Dataset"]
)

df = None
# Upload Mode

if data_source == "Upload File":
    uploaded_file = st.file_uploader(
        "Upload CSV or Excel file",
        type=["csv", "xlsx"]
    )

    if uploaded_file is not None:
        if uploaded_file.name.endswith(".xlsx"):
            df = pd.read_excel(uploaded_file)
        else:
            df = pd.read_csv(uploaded_file)


if data_source == "Use Demo Dataset":
    try:
        df = pd.read_excel("sample_data/1yr_transactions.xlsx")
        st.info("Loaded demo dataset")
    except Exception as e:
        st.error("Demo dataset not found. Please ensure file exists in sample_data folder.")
        st.stop()

# Run Analysis Button
run_analysis = st.button("Run Analysis")

if df is not None and run_analysis:

    df = clean_data(df)

    st.subheader("Cleaned Data Preview")
    st.dataframe(df.head())

    @st.cache_data
    def classify_cached(desc):
        return classify_transaction(desc)

    st.subheader("Classifying Transactions")
    df["category"] = df["description"].apply(classify_cached)

    st.success("Classification completed")

    init_db()
    save_data(df)

    # Filter expenses
    df_exp = df[df["amount"] < 0].copy()
    df_exp["amount"] = df_exp["amount"].abs()

    if df_exp.empty:
        st.warning("No expense transactions found. Showing full dataset instead.")
        df_exp = df.copy()
        df_exp["amount"] = df_exp["amount"].abs()

    # Category Distribution
    st.subheader("Category Distribution")
    fig_pie = px.pie(df_exp, names="category", values="amount")
    st.plotly_chart(fig_pie, use_container_width=True)

    # Monthly Trend
    monthly = prepare_monthly_data(df)

    if len(monthly) < 2:
        st.warning("Not enough data for prediction")
        st.stop()

    model = train_model(monthly)
    prediction = predict_next_month(model, monthly)

    monthly["month"] = monthly["month"].astype(str)

    st.subheader("Monthly Expense Trend")

    fig_line = px.line(
        monthly,
        x="month",
        y="amount",
        markers=True
    )

    fig_line.add_scatter(
        x=[monthly["month"].iloc[-1], "Next Month"],
        y=[monthly["amount"].iloc[-1], prediction],
        mode="lines+markers",
        line=dict(dash="dot"),
        name="Prediction"
    )

    st.plotly_chart(fig_line, use_container_width=True)

    st.metric(
        "Predicted Expense (Next Month)",
        f"{abs(prediction):.2f}"
    )
