"""Validation utilities for user input."""
from typing import Dict, Tuple


def validate_user(username: str, age: str, gender: str) -> Dict[str, str]:
    errors = {}
    if not username or not username.strip():
        errors["username"] = "Required"
    try:
        a = int(age)
        if a < 2 or a > 120:
            errors["age"] = "Age must be 2-120"
    except Exception:
        errors["age"] = "Invalid age"
    if gender not in ("Male", "Female", "Other"):
        errors["gender"] = "Select gender"
    return errors


def validate_measurements(weight: str, height_m: str = None, feet: str = None, inches: str = None, metric: bool = True):
    errors = {}
    try:
        w = float(weight)
        if w < 2 or w > 500:
            errors["weight"] = "Weight must be 2-500 kg"
    except Exception:
        errors["weight"] = "Invalid"

    if metric:
        try:
            h = float(height_m)
            if h < 0.5 or h > 2.5:
                errors["height"] = "Height must be 0.5-2.5 m"
        except Exception:
            errors["height"] = "Invalid"
    else:
        try:
            f = int(feet)
            i = int(inches)
            if f < 1 or f > 8:
                errors["feet"] = "Feet out of range"
            if i < 0 or i >= 12:
                errors["inches"] = "Inches 0-11"
        except Exception:
            errors["feet_inches"] = "Invalid"

    return errors
