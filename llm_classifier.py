from groq import Groq
from config import GROQ_API_KEY, MODEL_NAME, CATEGORIES

client = Groq(api_key=GROQ_API_KEY)

#  RULE-BASED 
def rule_based_category(desc):
    desc = desc.lower()

    if "salary" in desc:
        return "Salary"
    if "rent" in desc:
        return "Rent"
    if "electricity" in desc or "bill" in desc:
        return "Utilities"
    if "swiggy" in desc or "zomato" in desc or "restaurant" in desc:
        return "Food"
    if "uber" in desc or "ola" in desc:
        return "Travel"
    if "amazon" in desc or "flipkart" in desc or "shopping" in desc:
        return "Shopping"
    if "fuel" in desc or "petrol" in desc:
        return "Fuel"
    if "grocery" in desc:
        return "Groceries"
    if "netflix" in desc or "spotify" in desc:
        return "Entertainment"

    return None


# LLM FALLBACK
def llm_classify(desc):
    prompt = f"""
    Classify the transaction into one category:

    Categories: {CATEGORIES}

    Transaction: "{desc}"

    Return only category name.
    """

    try:
        response = client.chat.completions.create(
            model=MODEL_NAME,
            messages=[{"role": "user", "content": prompt}],
            temperature=0
        )

        return response.choices[0].message.content.strip()

    except Exception:
        return "Others"
def classify_transaction(desc):
    rule = rule_based_category(desc)

    if rule:
        return rule

    return llm_classify(desc)
