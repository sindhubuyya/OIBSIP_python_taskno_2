from bmi_calculator.core.validator import validate_measurements, validate_user


def test_validate_user_ok():
    errs = validate_user("alice", "30", "Female")
    assert errs == {}


def test_validate_user_bad_age():
    errs = validate_user("", "abc", "Unknown")
    assert "username" in errs and "age" in errs


def test_validate_measurements_metric_ok():
    errs = validate_measurements("70", height_m="1.75", metric=True)
    assert errs == {}


def test_validate_measurements_metric_bad():
    errs = validate_measurements("1000", height_m="0.2", metric=True)
    assert "weight" in errs and "height" in errs


def test_validate_measurements_imperial_ok():
    errs = validate_measurements("154", feet="5", inches="9", metric=False)
    assert errs == {}
