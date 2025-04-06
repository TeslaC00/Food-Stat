import json
from auth import get_model
import re

def format_prompt(food_data: dict) -> str:
    return f"""
You are a certified nutritionist. Based on the food product data in this JSON object, return a new JSON object with:

1. INGREDIENT_QUALITY_RATING
2. HEALTH_IMPACT_RATING
3. NUTRITIONAL_CONTENT_RATING

Each key should have:
- "score": a number between 0.0 to 5.0
- "reason": a one-line explanation of the score

Input JSON:
{json.dumps(food_data, indent=2)}
"""

def extract_json_from_response(text):
    start = text.find("{")
    if start == -1:
        raise ValueError("No opening brace found in response.")

    brace_count = 0
    for i in range(start, len(text)):
        if text[i] == "{":
            brace_count += 1
        elif text[i] == "}":
            brace_count -= 1
            if brace_count == 0:
                json_str = text[start:i+1]
                return json.loads(json_str)

    raise ValueError("JSON braces not balanced.")


def get_structured_rating(food_data):
    model = get_model("gemini-1.5-flash")
    prompt = format_prompt(food_data)
    response = model.generate_content(prompt)

    raw_text = response.text.strip()

    try:
        return extract_json_from_response(raw_text)
    except Exception as e:
        print("❌ Failed to parse JSON:", e)
        print("Raw response:\n", raw_text)
        return None


if __name__ == "__main__":
    food_json = {
        "item_category": "NAMKEEN",
        "item_name": "Salted Peanuts - Panjwani",
        "ingredients": ["Peanuts", "Salt", "Vegetable Oil"],
        "allergy_info": ["nuts", "Peanuts"],
        "nutrition": {
            "energy": "609",
            "protein": "0",
            "carbohydrate": "28.26",
            "total_fat": "47.78",
            "total_sugars": "7.26",
            "added_sugars": "N/A",
            "saturated_fat": "7.86",
            "trans_fat": "N/A"
        },
        "veg": True,
        "image_url": ""
    }

    result = get_structured_rating(food_json)
    print(json.dumps(result, indent=2))
