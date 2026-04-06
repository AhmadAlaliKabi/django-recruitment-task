"""
Purpose:
    Load the saved sklearn pipeline and predict monthly salary.

Connects with:
    - ml_models/linear_salary_prediction_pipeline.pkl
    - recruitment.views internal salary prediction API
"""

from pathlib import Path

import joblib
import pandas as pd


MODEL_PATH = Path(__file__).resolve().parent.parent / "ml_models" / "linear_salary_prediction_pipeline.pkl"

# These must match the feature columns used when training.
MODEL_FEATURES = [
    "Department",
    "Experience_Years",
    "Education_Level",
    "Age",
    "Gender",
    "City",
    "Experience_Age_Interaction",
    "Experience_Level",
]


def _experience_level_from_years(experience_years: int) -> int:
    """
    Convert experience years to a simple numeric level expected by the model.
    """
    if experience_years < 3:
        return 1
    if experience_years < 7:
        return 2
    if experience_years < 12:
        return 3
    return 4


def predict_salary(payload: dict) -> float:
    """
    Predict monthly salary from a validated payload dictionary.
    """
    if not MODEL_PATH.exists():
        raise FileNotFoundError(f"Model not found at {MODEL_PATH}")

    model = joblib.load(MODEL_PATH)

    # Build full input expected by the saved pipeline.
    input_payload = dict(payload)
    experience_years = int(input_payload["Experience_Years"])
    age = int(input_payload["Age"])
    input_payload["Experience_Age_Interaction"] = experience_years * age
    input_payload["Experience_Level"] = _experience_level_from_years(experience_years)

    input_df = pd.DataFrame([[input_payload[field] for field in MODEL_FEATURES]], columns=MODEL_FEATURES)
    predicted_value = model.predict(input_df)[0]
    return float(round(predicted_value, 2))
