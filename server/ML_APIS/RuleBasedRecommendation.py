import pandas as pd

data = pd.read_csv("ML_APIS/CleanedDataForModel.csv")


# Function to calculate BMI
def calculate_bmi(weight, height):
    return weight / (height**2)


# Function to personalize food recommendations based on user attributes
def personalize_food_recommendation(
    category, user_type, sex, height, weight, age, disease=None, df=data
):
    df = df[df["ITEM_CATEGORY"] == category]

    # Default scoring function
    df["PERSONALIZED_SCORE"] = 0

    # Calculate BMI
    bmi = calculate_bmi(weight, height)

     # Adjustments for BMI
    calorie_factor = 1.5 if bmi < 18.5 else 1.0 if 18.5 <= bmi <= 24.9 else 0.8

    # Age-based protein factor
    if age < 18:
        protein_factor = 1.3
    elif 18 <= age <= 30:
        protein_factor = 1.2 if sex == 'Male' else 1.0
    elif 31 <= age <= 50:
        protein_factor = 1.1 if sex == 'Male' else 0.9
    else:
        protein_factor = 1.3  # Increased for muscle maintenance in older adults
    
         # Default Weights for Nutritional Factors (if no disease)
    CALORIE_WEIGHT = 0.1
    PROTEIN_WEIGHT = 0.3 * protein_factor
    CARB_WEIGHT = 0.1
    SUGAR_WEIGHT = 0.2
    ADDED_SUGAR_WEIGHT = 0.3
    FAT_WEIGHT = 0.2
    SATURATED_FAT_WEIGHT = 0.2
    FIBER_WEIGHT = 0.2
    SODIUM_WEIGHT = 0.1

    # Adjust weights based on disease
    if disease == "Diabetes":
        # Prioritize low sugar and carbs, increase fiber weight
        SUGAR_WEIGHT = 0.5
        ADDED_SUGAR_WEIGHT = 0.25
        CARB_WEIGHT = 0.2
        FIBER_WEIGHT = 0.4
        CALORIE_WEIGHT = 0.05

    elif disease == "Anemia":
        # Prioritize high protein and iron (if iron data available), decrease sugar weight
        PROTEIN_WEIGHT = 0.5
        CALORIE_WEIGHT = 0.15
        SUGAR_WEIGHT = 0.1
        ADDED_SUGAR_WEIGHT = 0.1
        # Optionally increase a new "IRON_WEIGHT" if iron is part of the data

    elif disease == "Hypertension":
        # Prioritize low sodium and fat, increase fiber weight
        SODIUM_WEIGHT = 0.4
        SATURATED_FAT_WEIGHT = 0.3
        FIBER_WEIGHT = 0.3
        CALORIE_WEIGHT = 0.1

    elif disease == "Cardiovascular Disease":
        # Prioritize low fat, saturated fat, and sodium
        FAT_WEIGHT = 0.4
        SATURATED_FAT_WEIGHT = 0.5
        SODIUM_WEIGHT = 0.3
        FIBER_WEIGHT = 0.2
        CALORIE_WEIGHT = 0.05

    # Define scoring rules based on user type
    if user_type == "Weight Loss":
        df["PERSONALIZED_SCORE"] = (
            (df["NUTRITION.ENERGY"] < 200) * CALORIE_WEIGHT * calorie_factor
            + (df["NUTRITION.FIBER"] > 2) * FIBER_WEIGHT
            - (df["NUTRITION.TOTAL_SUGARS"] > 5) * SUGAR_WEIGHT
            - (df["NUTRITION.SATURATED_FAT"] > 2) * SATURATED_FAT_WEIGHT
        )

    elif user_type == "Weight Gain":
        df["PERSONALIZED_SCORE"] = (
            (df["NUTRITION.ENERGY"] > 400) * CALORIE_WEIGHT * calorie_factor
            + (df["NUTRITION.PROTEIN"] > 10) * PROTEIN_WEIGHT * protein_factor
            + (df["NUTRITION.CARBOHYDRATE"] > 20) * CARB_WEIGHT
            + (df["NUTRITION.TOTAL_FAT"] > 10) * FAT_WEIGHT
        )

    elif user_type == "Muscle up":
        df["PERSONALIZED_SCORE"] = (
            (df["NUTRITION.PROTEIN"] > 20) * PROTEIN_WEIGHT * protein_factor
            + (df["NUTRITION.CARBOHYDRATE"] > 30) * CARB_WEIGHT
            - (df["NUTRITION.SATURATED_FAT"] > 2) * SATURATED_FAT_WEIGHT
        )

    elif user_type == "General Fitness":
        df["PERSONALIZED_SCORE"] = (
            (df["NUTRITION.ENERGY"] < 300) * CALORIE_WEIGHT * calorie_factor
            + (df["NUTRITION.PROTEIN"] > 10) * PROTEIN_WEIGHT * protein_factor
            + (df["NUTRITION.FIBER"] > 2) * FIBER_WEIGHT
        )

    elif user_type == "Pregnant Mother":
        df["PERSONALIZED_SCORE"] = (
            (df["NUTRITION.FIBER"] > 2) * FIBER_WEIGHT
            + (df["NUTRITION.PROTEIN"] > 10) * PROTEIN_WEIGHT * protein_factor
            + (df["NUTRITION.ADDED_SUGARS"] < 5) * ADDED_SUGAR_WEIGHT
            + (df["NUTRITION.SODIUM"] < 200) * SODIUM_WEIGHT
        )

    elif user_type == "Infant":
        df["PERSONALIZED_SCORE"] = (
            (df["NUTRITION.ENERGY"] < 100) * CALORIE_WEIGHT * calorie_factor
            + (df["NUTRITION.FIBER"] < 1) * FIBER_WEIGHT
            - (df["NUTRITION.ADDED_SUGARS"] > 0) * ADDED_SUGAR_WEIGHT
            + (df["NUTRITION.TOTAL_FAT"] > 5) * FAT_WEIGHT
        )

    # Sort foods based on score
    df = df.sort_values(by="PERSONALIZED_SCORE", ascending=False)

    return df[["ITEM_NAME", "PERSONALIZED_SCORE"]].values.tolist()
