import os
from joblib import load
import pandas as pd


# Load the pre-trained model from the pickle file
def load_model(model_path="ML_APIS/pipeline.joblib"):
    """Load the trained model from a file."""

    with open("ML_APIS/pipeline.joblib", "rb") as model_file:
        model = load(model_file)
    return model


# Function to predict the food rating
def predict_food_rating(input_data, model, example_data=None):
    """
    Predict the final food rating based on user input.

    :param model: The trained model (pipeline)
    :param input_data: A DataFrame or dict containing the features for prediction
    :return: The predicted food rating
    """
    # Convert input_data to DataFrame if it's in dict format
    if isinstance(input_data, dict):
        input_data = pd.DataFrame([input_data])

    # Make predictions using the loaded model
    prediction = model.predict(input_data)
    return float(prediction[0])


# Example usage
if __name__ == "__main__":
    # Load the model
    model_path = os.path.abspath("ML_APIS/pipeline.joblib")
    model_path = os.path.abspath("ML_APIS/pipeline.joblib")
    model = load_model(model_path)

    # Example input data (you can replace this with real user input)
    example_data = {
        "NUTRITION.ENERGY": 120,  # Example energy value
        "NUTRITION.PROTEIN": 3.5,  # Example protein value
        "NUTRITION.CARBOHYDRATE": 15,  # Example carbs value
        "NUTRITION.TOTAL_SUGARS": 2,  # Example sugars value
        "NUTRITION.ADDED_SUGARS": 1,  # Example added sugars value
        "NUTRITION.TOTAL_FAT": 5,  # Example fat value
        "NUTRITION.SATURATED_FAT": 1,  # Example saturated fat value
        "NUTRITION.FIBER": 2,  # Example fiber value
        "NUTRITION.SODIUM": 150,  # Example sodium value
    }

    # Predict the rating
    # predicted_rating = predict_food_rating(model=model, input_data=example_data)
    predicted_rating = predict_food_rating(model=model, input_data=example_data)

    print(f"The predicted food rating is: {predicted_rating}")
