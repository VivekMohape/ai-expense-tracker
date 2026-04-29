import pandas as pd

def generate_insights(df, monthly, prediction):
    insights = []

    # Highest spending category
    df_exp = df[df["amount"] < 0].copy()
    df_exp["amount"] = df_exp["amount"].abs()

    if not df_exp.empty:
        top_category = df_exp.groupby("category")["amount"].sum().idxmax()
        insights.append(f"Highest spending category is {top_category}.")

    # Highest spending month
    if not monthly.empty:
        max_month = monthly.loc[monthly["amount"].idxmin(), "month"]
        insights.append(f"Highest spending month is {max_month}.")

    # Trend detection
    if len(monthly) > 2:
        if monthly["amount"].iloc[-1] < monthly["amount"].iloc[-2]:
            insights.append("Spending has increased compared to the previous month.")
        else:
            insights.append("Spending has decreased compared to the previous month.")

    # Prediction insight
    if prediction < monthly["amount"].iloc[-1]:
        insights.append("Expenses are expected to increase next month.")
    else:
        insights.append("Expenses are expected to decrease next month.")

    return insights
