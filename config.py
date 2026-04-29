import streamlit as st


GROQ_API_KEY = st.secrets["GROQ_API_KEY"]

MODEL_NAME = "openai/gpt-oss-120b"
DB_PATH = "data/transactions.db"

# Fixed categories
CATEGORIES = [
    "Food",
    "Travel",
    "Shopping",
    "Utilities",
    "Rent",
    "Entertainment",
    "Salary",
    "Others"
]
