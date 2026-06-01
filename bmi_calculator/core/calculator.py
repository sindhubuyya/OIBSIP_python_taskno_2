"""BMI calculation logic and helpers."""
from typing import Tuple
from bmi_calculator.utils.constants import BMI_RANGES


def calculate_bmi(weight_kg: float, height_m: float) -> float:
    """Calculate BMI given weight in kg and height in meters."""
    if height_m <= 0:
        raise ValueError("height must be positive")
    bmi = weight_kg / (height_m * height_m)
    return round(bmi, 2)


def kg_from_lbs(lbs: float) -> float:
    return lbs * 0.45359237


def m_from_ft_in(feet: int, inches: int) -> float:
    total_inches = feet * 12 + inches
    meters = total_inches * 0.0254
    return meters


def classify_bmi(bmi: float) -> str:
    """Classify BMI using WHO categories from constants."""
    for name, (low, high, _) in BMI_RANGES.items():
        if (low is None or bmi >= low) and (high is None or bmi < high):
            return name
    return "Unknown"


def healthy_weight_range_for_height(height_m: float) -> Tuple[float, float]:
    """Return min and max healthy weight (kg) for a given height using 18.5 - 24.9 BMI range."""
    min_w = 18.5 * (height_m ** 2)
    max_w = 24.9 * (height_m ** 2)
    return round(min_w, 1), round(max_w, 1)
