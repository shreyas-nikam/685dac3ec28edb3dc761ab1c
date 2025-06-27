
def calculate_human_capital_factor(
    job_role: str,
    education_level: str,
    field_of_study: str,
    school_tier: str,
    years_experience: int
) -> float:
    """
    Calculates the Human Capital Factor (FHC) based on an individual's professional background.

    Args:
        job_role (str): The individual's current job role.
        education_level (str): The highest education level attained.
        field_of_study (str): The field of study during education.
        school_tier (str): The tier ranking of the educational institution.
        years_experience (int): Total years of professional experience.

    Returns:
        float: The calculated Human Capital Factor.

    Raises:
        KeyError: If the job_role is not recognized.
        ValueError: If input arguments are invalid.
    """

    # Mappings for job roles to base factors
    job_role_factors = {
        "Paralegal": 1.262,
        "Senior Research Scientist": 0.192,
        "Analyst": 1.10,
        "Architect": 1.0
        # Add more roles as needed
    }

    # Mappings for education levels
    education_levels = {
        "PhD": 1.10,
        "Master's": 1.05,
        "Bachelor's": 1.00
        # Add more as needed
    }

    # Mappings for field of study
    field_of_study_factors = {
        "Tech/Engineering/Quantitative Science": 1.00,
        "Liberal Arts/Humanities": 1.10,
        "Business/Finance": 1.00
        # Extend as necessary
    }

    # Mappings for school tiers
    school_tier_factors = {
        "Tier 1": 0.95,
        "Tier 2": 1.00,
        "Tier 3": 1.05
        # Add more tiers if needed
    }

    # Validate inputs
    if job_role not in job_role_factors:
        raise KeyError(f"Unknown job role: {job_role}")

    if education_level not in education_levels:
        raise ValueError(f"Unknown education level: {education_level}")

    if field_of_study not in field_of_study_factors:
        raise ValueError(f"Unknown field of study: {field_of_study}")

    if school_tier not in school_tier_factors:
        raise ValueError(f"Unknown school tier: {school_tier}")

    if not isinstance(years_experience, (int, float)) or years_experience < 0:
        raise ValueError("Years of experience must be a non-negative number.")

    # Retrieve factors
    base_factor = job_role_factors[job_role]
    edu_factor = education_levels[education_level]
    field_factor = field_of_study_factors[field_of_study]
    tier_factor = school_tier_factors[school_tier]

    # Adjust for experience: cap at 20 years
    capped_experience = min(years_experience, 20)
    experience_adjustment = 1 - 0.015 * capped_experience

    # Calculate final FHC
    fhc = base_factor * edu_factor * field_factor * tier_factor * experience_adjustment

    return fhc
