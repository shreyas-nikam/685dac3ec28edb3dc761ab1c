import pytest
from definition_9465bafffe6d4d2b91c5276176b39a25 import calculate_human_capital_factor

@pytest.mark.parametrize("role_multiplier, education_level_factor, education_field_factor, school_tier_factor, experience_factor, expected", [
    (1.35, 1.00, 1.10, 1.00, 0.85, 1.262),
    (0.3, 0.85, 0.90, 0.95, 0.88, 0.192),
    (2.0, 1.50, 1.20, 1.10, 1.00, 3.96),
    (1.0, 1.0, 1.0, 1.0, 0.0, 0.0),
])
def test_calculate_human_capital_factor(role_multiplier, education_level_factor, education_field_factor, school_tier_factor, experience_factor, expected):
    result = calculate_human_capital_factor(role_multiplier, education_level_factor, education_field_factor, school_tier_factor, experience_factor)
    assert abs(result - expected) < 1e-6

@pytest.mark.parametrize("invalid_inputs, exception_type", [
    (("a", 1.0, 1.0, 1.0, 1.0), TypeError),
    (("1.0", "1.0", "1.0", "1.0", "1.0"), TypeError),
    ((None, 1.0, 1.0, 1.0, 1.0), TypeError),
])
def test_calculate_human_capital_factor_exceptions(invalid_inputs, exception_type):
    with pytest.raises(exception_type):
        calculate_human_capital_factor(*invalid_inputs)
