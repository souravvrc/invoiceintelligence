import joblib
import pandas as pd
from pathlib import Path

# Correct path to model
MODEL_PATH = (
    Path(__file__).resolve().parent.parent
    / "freight_cost_prediction"
    / "models"
    / "predict_freight_model.pkl"
)

def load_model(model_path: str = MODEL_PATH):
    """
    Load trained freight cost prediction model.
    """
    model = joblib.load(model_path)
    return model


def predict_freight_cost(input_data):
    model = load_model()

    input_df = pd.DataFrame(input_data)

    input_df["Predicted_Freight"] = model.predict(input_df).round()

    return input_df


if __name__ == "__main__":

    # Example interface run (local testing)
    sample_data = {
        "Dollars": [18500, 9000, 3000, 200]
    }

    prediction = predict_freight_cost(sample_data)

    print(prediction)