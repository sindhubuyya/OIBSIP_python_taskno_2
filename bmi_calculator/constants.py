"""Constants for BMI category colors and health messages."""

BMI_CATEGORIES = {
    "Underweight": {"range": (None, 18.5), "status": "Underweight"},
    "Normal Weight": {"range": (18.5, 25.0), "status": "Normal"},
    "Overweight": {"range": (25.0, 30.0), "status": "Overweight"},
    "Obese": {"range": (30.0, None), "status": "Obese"},
}

CATEGORY_COLORS = {
    "Underweight": "#7FDBFF",
    "Normal Weight": "#3CB371",
    "Overweight": "#FFB366",
    "Obese": "#FF6B6B",
}

HEALTH_TIPS = {
    "Underweight": "Consider a nutrient-rich diet and speak with your doctor about healthy weight gain.",
    "Normal Weight": "Keep up the healthy habits and stay active.",
    "Overweight": "Try regular exercise and a balanced diet to support healthy weight.",
    "Obese": "Work with a health professional on a safe plan to reduce BMI.",
}
