
def calculate_human_capital_factor(
    role_multiplier: float,
    education_level_factor: float,
    education_field_factor: float,
    school_tier_factor: float,
    experience_factor: float
) -> float:
    """
    Calculates the Human Capital Factor based on individual educational and professional attributes.

    Args:
        role_multiplier (float): Multiplier based on job role vulnerability.
        education_level_factor (float): Factor representing the education level.
        education_field_factor (float): Factor representing the field of education.
        school_tier_factor (float): Factor based on the institution's tier.
        experience_factor (float): Decay factor based on years of experience.

    Returns:
        float: The computed Human Capital Factor.

    Raises:
        TypeError: If any input is not a float or int.
    """
    # Validate inputs
    for arg in [role_multiplier, education_level_factor, education_field_factor, school_tier_factor, experience_factor]:
        if not isinstance(arg, (float, int)):
            raise TypeError(f"Invalid input type: {arg}. Expected float or int.")
    # Return 0 if experience_factor is zero (or very close to zero)
    if abs(experience_factor) < 1e-12:
        return 0.0
    return role_multiplier * education_level_factor * education_field_factor * school_tier_factor * experience_factor
