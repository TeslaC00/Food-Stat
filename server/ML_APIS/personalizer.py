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
            "energy": 0.005
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
    },
    "obese": {
        "boost": {
            "protein": 0.1
        },
        "penalize": {
            "energy": 0.01,
            "saturated_fat": 0.15,
            "total_fat": 0.15,
            "total_sugars": 0.2
        }
    }
}

# Disease nutrient constraints (hard filters or penalty triggers)
DISEASE_RULES = {
    "diabetes": {
        "avoid": ["total_sugars", "added_sugars"]
    },
    "hypertension": {
        "avoid": ["salt", "sodium"]
    },
    "cardiovascular_disease": {
        "avoid": ["trans_fat", "saturated_fat"]
    },
    "anemia": {
        "avoid": []
    },
    "kidney_disease": {
        "avoid": ["salt", "sodium", "protein"]
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
    try:
        normalized_type = user_type.strip().lower().replace(" ", "_")

        user_diet_type = food_item.get("dietType", "non_vegetarian").strip().lower()
        if user_diet_type == "vegetarian" and not food_item.get("veg", True):
            return 0.1

        user_allergies = food_item.get("user_allergies") or []
        item_allergies = food_item.get("allergy_info") or []
        item_allergies = [a.lower() for a in item_allergies if isinstance(a, str)]

        if any(allergen.lower() in item_allergies for allergen in user_allergies if isinstance(allergen, str)):
            return 0.1

        user_diseases = food_item.get("user_diseases") or []
        nutrition = food_item.get("nutrition") or {}

        for disease in user_diseases:
            disease_key = disease.strip().lower().replace(" ", "_")
            disease_rule = DISEASE_RULES.get(disease_key)
            if disease_rule:
                for restricted in disease_rule.get("avoid", []):
                    if parse_float(nutrition.get(restricted, 0)) > 0:
                        return 0.1

        rules = RULE_SETS.get(normalized_type)
        if not rules:
            raise ValueError(f"Unsupported user type: {user_type}")

        score = base_health_score

        for nutrient, weight in rules.get("boost", {}).items():
            value = parse_float(nutrition.get(nutrient, 0))
            score += weight * value

        for nutrient, weight in rules.get("penalize", {}).items():
            value = parse_float(nutrition.get(nutrient, 0))
            score -= weight * value

        return clamp_score(score)

    except Exception as e:
        print(f"Error scoring item '{food_item.get('item_name', 'Unknown')}': {e}")
        return 0.0


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
            "calcium": "150",
            "salt": "1.0"
        },
        "veg": True,
        "image_url": "",
        "user_allergies": ["nuts"],
        "user_diseases": ["diabetes"],
        "dietType": "vegetarian"
    }

    for user in [
        "weight_loss",
        "weight_gain",
        "muscle_gain",
        "pregnant_mother",
        "infant",
        "general_fitness",
        "obese"
    ]:
        personalized = personalize_score(food_item, user)
        print(f"{user.replace('_', ' ').capitalize()} Score: {personalized}")
