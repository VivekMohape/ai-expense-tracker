from groq import Groq
from config import GROQ_API_KEY, MODEL_NAME, CATEGORIES

client = Groq(api_key=GROQ_API_KEY)

def classify_batch(descriptions):
    prompt = f"""
    Classify each transaction into one of these categories:
    {CATEGORIES}

    Return output as JSON list:
    [
      {{"text": "...", "category": "..."}}
    ]

    Transactions:
    {descriptions}
    """

    try:
        response = client.chat.completions.create(
            model=MODEL_NAME,
            messages=[{"role": "user", "content": prompt}],
            temperature=0
        )

        content = response.choices[0].message.content
        return content

    except Exception:
        return None


def classify_with_fallback(description):
    try:
        response = client.chat.completions.create(
            model=MODEL_NAME,
            messages=[{
                "role": "user",
                "content": f"""
                Classify transaction:
                "{description}"

                Categories:
                {CATEGORIES}

                Return only category name.
                """
            }],
            temperature=0
        )

        return response.choices[0].message.content.strip()

    except Exception:
        return "Others"
