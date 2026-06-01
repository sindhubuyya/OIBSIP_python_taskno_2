"""Constants for BMI categories, colors, and messages."""

BMI_RANGES = {
    "Underweight": (None, 18.5, "#5DA9E9"),
    "Normal weight": (18.5, 25.0, "#2ECC71"),
    "Overweight": (25.0, 30.0, "#F1C40F"),
    "Obese (Class I)": (30.0, 35.0, "#E67E22"),
    "Obese (Class II)": (35.0, 40.0, "#E74C3C"),
    "Obese (Class III)": (40.0, None, "#C0392B"),
}

HEALTH_TIPS = {
    "Underweight": "Consider a nutrient-rich diet and consult a healthcare professional.",
    "Normal weight": "Maintain your healthy lifestyle and balanced diet.",
    "Overweight": "Incorporate regular exercise and review calorie intake.",
    "Obese (Class I)": "Speak to a healthcare provider for tailored advice.",
    "Obese (Class II)": "Consider professional guidance and structured weight loss plan.",
    "Obese (Class III)": "Seek medical support; significant health interventions may be required.",
}
