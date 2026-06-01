"""BMI calculation helper functions."""
from bmi_calculator.constants import BMI_CATEGORIES


def calculate_metric_bmi(weight_kg: float, height_cm: float) -> float:
    return round(weight_kg / ((height_cm / 100.0) ** 2), 2)


def calculate_imperial_bmi(weight_lbs: float, feet: int, inches: int) -> float:
    total_inches = feet * 12 + inches
    return round((weight_lbs * 703) / (total_inches ** 2), 2)


def classify_bmi(bmi: float) -> str:
    for category, data in BMI_CATEGORIES.items():
        low, high = data["range"]
        if (low is None or bmi >= low) and (high is None or bmi < high):
            return category
    return "Normal Weight"
