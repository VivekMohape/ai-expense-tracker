import streamlit as st

GROQ_API_KEY = st.secrets["GROQ_API_KEY"]
MODEL_NAME = "openai/gpt-oss-120b"

DB_PATH = "data/transactions.db"

CATEGORIES = [
    "Food",
    "Travel",
    "Shopping",
    "Utilities",
    "Rent",
    "Entertainment",
    "Salary",
    "Groceries",
    "Fuel",
    "Others"
]
