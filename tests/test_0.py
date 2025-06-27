import pytest
from definition_6ad387f187394b469b00e61c85535a06 import calculate_human_capital_factor

@pytest.mark.parametrize("job_role, education_level, field_of_study, school_tier, years_experience, expected", [
    # Basic test with typical values
    ("Paralegal", "Bachelor's", "Tech/Engineering/Quantitative Science", "Tier 1", 10, 1.262 * 0.95 * 1.00 * 0.90 * (1 - 0.015 * 10)),
    ("Senior Research Scientist", "PhD", "Liberal Arts/Humanities", "Tier 2", 25, 0.192 * 1.00 * 1.10 * 1.00 * (1 - 0.015 * 20)),
    # Edge case: zero experience
    ("Analyst", "Master's", "Business/Finance", "Tier 3", 0, 1.10 * 1.00 * 1.00 * 1.05 * (1 - 0.015 * 0)),
    # High experience (beyond 20 years)
    ("Architect", "Bachelor's", "Tech/Engineering/Quantitative Science", "Tier 1", 40, 1.0 * 0.95 * 0.90 * 0.95 * (1 - 0.015 * 20)),
    # Invalid job role (should raise KeyError or handle gracefully)
    # For testing purposes, assume it raises KeyError
    # ("Unknown Role", "Bachelor's", "Tech/Engineering/Quantitative Science", "Tier 1", 5, KeyError),
])
def test_calculate_human_capital_factor(job_role, education_level, field_of_study, school_tier, years_experience, expected):
    from definition_6ad387f187394b469b00e61c85535a06 import calculate_human_capital_factor
    if isinstance(expected, type) and issubclass(expected, Exception):
        with pytest.raises(expected):
            calculate_human_capital_factor(job_role, education_level, field_of_study, school_tier, years_experience)
    else:
        result = calculate_human_capital_factor(job_role, education_level, field_of_study, school_tier, years_experience)
        assert abs(result - expected) < 1e-6
