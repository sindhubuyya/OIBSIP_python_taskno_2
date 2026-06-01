from bmi_calculator.utils.bmi_utils import (
    calculate_imperial_bmi,
    calculate_metric_bmi,
    classify_bmi,
)


def test_metric_bmi_calculation():
    assert calculate_metric_bmi(70, 175) == 22.86


def test_imperial_bmi_calculation():
    assert calculate_imperial_bmi(154, 5, 9) == 22.74


def test_classification_boundaries():
    assert classify_bmi(18.4) == "Underweight"
    assert classify_bmi(18.5) == "Normal Weight"
    assert classify_bmi(24.9) == "Normal Weight"
    assert classify_bmi(25.0) == "Overweight"
    assert classify_bmi(30.0) == "Obese"
