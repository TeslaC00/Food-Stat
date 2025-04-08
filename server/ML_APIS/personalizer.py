# foodstat_personalizer.py

from typing import Dict, Union


# User Type Rules
RULE_SETS = {
    "weight_loss": {
        "boost": {
            "protein": 0.15
        },
        "penalize": {
            "total_sugars": 0.25,
            "saturated_fat": 0.2,
            "total_fat": 0.1,
            "energy": 0.005  # Reduced penalty
        }
    },
    "weight_gain": {
        "boost": {
            "protein": 0.2,
            "total_fat": 0.2,
            "energy": 0.1
        },
        "penalize": {
            "fiber": 0.1
        }
    },
    "muscle_gain": {
        "boost": {
            "protein": 0.3,
            "total_fat": 0.05
        },
        "penalize": {
            "total_sugars": 0.1
        }
    },
    "pregnant_mother": {
        "boost": {
            "protein": 0.2,
            "energy": 0.05,
            "iron": 0.2,
            "calcium": 0.2
        },
        "penalize": {
            "saturated_fat": 0.1,
            "trans_fat": 0.2,
            "total_sugars": 0.1
        }
    },
    "infant": {
        "boost": {
            "iron": 0.2,
            "calcium": 0.2
        },
        "penalize": {
            "salt": 0.4,
            "total_sugars": 0.3,
            "trans_fat": 0.3,
            "saturated_fat": 0.2
        }
    },
    "general_fitness": {
        "boost": {
            "protein": 0.2,
            "fiber": 0.2
        },
        "penalize": {
            "total_sugars": 0.1
        }
    }
}


def parse_float(value: Union[str, float, int]) -> float:
    try:
        return float(value)
    except (ValueError, TypeError):
        return 0.0


def clamp_score(score: float) -> float:
    return max(0.0, min(5.0, round(score, 2)))


def personalize_score(food_item: Dict, user_type: str, base_health_score: float = 3.5) -> float:
    normalized_type = user_type.strip().lower().replace(" ", "_")
    rules = RULE_SETS.get(normalized_type)
    if not rules:
        raise ValueError(f"Unsupported user type: {user_type}")

    # Vegetarian check
    if user_type.lower() == "vegetarian" and not food_item.get("veg", True):
        return 0.0

    # Allergy check
    user_allergies = food_item.get("user_allergies", [])
    item_allergies = [a.lower() for a in food_item.get("allergy_info", [])]
    if any(allergen.lower() in item_allergies for allergen in user_allergies):
        return 0.0

    nutrition = food_item.get("nutrition", {})
    score = base_health_score

    for nutrient, weight in rules.get("boost", {}).items():
        value = parse_float(nutrition.get(nutrient, 0))
        score += weight * value

    for nutrient, weight in rules.get("penalize", {}).items():
        value = parse_float(nutrition.get(nutrient, 0))
        score -= weight * value

    return clamp_score(score)


# Demo

def example():
    food_item = {
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
            "trans_fat": "N/A",
            "iron": "2.0",
            "calcium": "150"
        },
        "veg": True,
        "image_url": "",
        "user_allergies": ["nuts"]
    }

    for user in [
        "weight_loss",
        "weight_gain",
        "muscle_gain",
        "pregnant_mother",
        "infant",
        "general_fitness"
    ]:
        personalized = personalize_score(food_item, user)
        print(f"{user.replace('_', ' ').capitalize()} Score: {personalized}")
