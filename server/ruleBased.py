import pandas as pd
from typing import List, Optional

# Constants
NUTRITION_COLUMNS = {
    'energy': 'NUTRITION.ENERGY',
    'protein': 'NUTRITION.PROTEIN',
    'carb': 'NUTRITION.CARBOHYDRATE',
    'sugar': 'NUTRITION.TOTAL_SUGARS',
    'added_sugar': 'NUTRITION.ADDED_SUGARS',
    'fat': 'NUTRITION.TOTAL_FAT',
    'saturated_fat': 'NUTRITION.SATURATED_FAT',
    'fiber': 'NUTRITION.FIBER',
    'sodium': 'NUTRITION.SODIUM'
}

BMI_CATEGORIES = {
    'underweight': 18.5,
    'normal': 24.9,
    'overweight': 29.9
}

def calculate_bmi(weight: float, height: float) -> float:
    """Calculate Body Mass Index (BMI) using weight (kg) and height (m)."""
    return weight / (height ** 2)

def personalize_food_recommendation(
    category: str,
    user_type: str,
    sex: str,
    height: float,
    weight: float,
    age: int,
    disease: Optional[str] = None,
    df: pd.DataFrame = data
) -> List[List[str]]:
    """
    Generate personalized food recommendations based on user attributes and health goals.
    
    Args:
        category: Food category to filter by
        user_type: Health goal (e.g., 'Weight Loss', 'Muscle up')
        sex: Biological sex ('Male'/'Female')
        height: Height in meters
        weight: Weight in kilograms
        age: Age in years
        disease: Optional health condition to consider
        df: DataFrame containing food data
        
    Returns:
        List of recommended food items with scores, sorted by relevance
    """
    # Create working copy of filtered data
    df_filtered = df[df["ITEM_CATEGORY"] == category].copy()
    
    if df_filtered.empty:
        return []

    # Initialize nutritional weights
    weights = initialize_weights(age, sex)
    adjust_weights_for_disease(weights, disease)
    
    # Calculate health factors
    bmi = calculate_bmi(weight, height)
    calorie_factor = calculate_calorie_factor(bmi)
    protein_factor = calculate_protein_factor(age, sex)
    
    # Calculate personalized scores
    scoring_function = get_scoring_function(user_type, weights, calorie_factor, protein_factor)
    df_filtered["PERSONALIZED_SCORE"] = scoring_function(df_filtered)
    
    # Return sorted recommendations
    return format_recommendations(df_filtered)

def initialize_weights(age: int, sex: str) -> dict:
    """Initialize base nutritional weights based on age and sex."""
    protein_factor = calculate_protein_factor(age, sex)
    
    return {
        'calorie': 0.1,
        'protein': 0.3 * protein_factor,
        'carb': 0.1,
        'sugar': 0.2,
        'added_sugar': 0.3,
        'fat': 0.2,
        'saturated_fat': 0.2,
        'fiber': 0.2,
        'sodium': 0.1
    }

def adjust_weights_for_disease(weights: dict, disease: Optional[str]) -> None:
    """Adjust nutritional weights based on health conditions."""
    if not disease:
        return

    adjustments = {
        'Diabetes': {
            'sugar': 0.5,
            'added_sugar': 0.25,
            'carb': 0.2,
            'fiber': 0.4,
            'calorie': 0.05
        },
        'Anemia': {
            'protein': 0.5,
            'calorie': 0.15,
            'sugar': 0.1,
            'added_sugar': 0.1
        },
        'Hypertension': {
            'sodium': 0.4,
            'saturated_fat': 0.3,
            'fiber': 0.3,
            'calorie': 0.1
        },
        'Cardiovascular Disease': {
            'fat': 0.4,
            'saturated_fat': 0.5,
            'sodium': 0.3,
            'fiber': 0.2,
            'calorie': 0.05
        }
    }
    
    if disease in adjustments:
        weights.update(adjustments[disease])

def calculate_protein_factor(age: int, sex: str) -> float:
    """Determine protein needs based on age and sex."""
    if age < 18:
        return 1.3
    elif 18 <= age <= 30:
        return 1.2 if sex == 'Male' else 1.0
    elif 31 <= age <= 50:
        return 1.1 if sex == 'Male' else 0.9
    else:
        return 1.3  # Increased for older adults

def calculate_calorie_factor(bmi: float) -> float:
    """Determine calorie adjustment based on BMI."""
    if bmi < BMI_CATEGORIES['underweight']:
        return 1.5
    elif BMI_CATEGORIES['underweight'] <= bmi <= BMI_CATEGORIES['normal']:
        return 1.0
    return 0.8

def get_scoring_function(user_type: str, weights: dict, calorie_factor: float, protein_factor: float):
    """Return appropriate scoring function based on user type."""
    scoring_rules = {
        'Weight Loss': lambda df: (
            (df[NUTRITION_COLUMNS['energy']] < 200) * weights['calorie'] * calorie_factor +
            (df[NUTRITION_COLUMNS['fiber']] > 2) * weights['fiber'] -
            (df[NUTRITION_COLUMNS['sugar']] > 5) * weights['sugar'] -
            (df[NUTRITION_COLUMNS['saturated_fat']] > 2) * weights['saturated_fat']
        ),
        'Weight Gain': lambda df: (
            (df[NUTRITION_COLUMNS['energy']] > 400) * weights['calorie'] * calorie_factor +
            (df[NUTRITION_COLUMNS['protein']] > 10) * weights['protein'] +
            (df[NUTRITION_COLUMNS['carb']] > 20) * weights['carb'] +
            (df[NUTRITION_COLUMNS['fat']] > 10) * weights['fat']
        ),
        'Muscle up': lambda df: (
            (df[NUTRITION_COLUMNS['protein']] > 20) * weights['protein'] +
            (df[NUTRITION_COLUMNS['carb']] > 30) * weights['carb'] -
            (df[NUTRITION_COLUMNS['saturated_fat']] > 2) * weights['saturated_fat']
        ),
        'General Fitness': lambda df: (
            (df[NUTRITION_COLUMNS['energy']] < 300) * weights['calorie'] * calorie_factor +
            (df[NUTRITION_COLUMNS['protein']] > 10) * weights['protein'] +
            (df[NUTRITION_COLUMNS['fiber']] > 2) * weights['fiber']
        ),
        'Pregnant Mother': lambda df: (
            (df[NUTRITION_COLUMNS['fiber']] > 2) * weights['fiber'] +
            (df[NUTRITION_COLUMNS['protein']] > 10) * weights['protein'] +
            (df[NUTRITION_COLUMNS['added_sugar']] < 5) * weights['added_sugar'] +
            (df[NUTRITION_COLUMNS['sodium']] < 200) * weights['sodium']
        ),
        'Infant': lambda df: (
            (df[NUTRITION_COLUMNS['energy']] < 100) * weights['calorie'] * calorie_factor +
            (df[NUTRITION_COLUMNS['fiber']] < 1) * weights['fiber'] -
            (df[NUTRITION_COLUMNS['added_sugar']] > 0) * weights['added_sugar'] +
            (df[NUTRITION_COLUMNS['fat']] > 5) * weights['fat']
        )
    }
    
    return scoring_rules.get(user_type, lambda df: df[NUTRITION_COLUMNS['energy']] * 0)

def format_recommendations(df: pd.DataFrame) -> List[List[str]]:
    """Format and sort recommendations."""
    return (
        df.sort_values("PERSONALIZED_SCORE", ascending=False)
        [["ITEM_NAME", "PERSONALIZED_SCORE"]]
        .values.tolist()
    )

# Load data
data = pd.read_csv("ML_APIS/CleanedDataForModel.csv")