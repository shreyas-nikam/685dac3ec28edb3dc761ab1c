id: 685dac3ec28edb3dc761ab1c_documentation
summary: AI-Q Score: A Multi-Factor Parametric Framework for Quantifying and Mitigating AI-Driven Job Displacement Risk Documentation
feedback link: https://docs.google.com/forms/d/e/1FAIpQLSfWkOK-in_bMMoHSZfcIvAeO58PAH9wrDqcxnJABHaxiDqhSA/viewform?usp=sf_link
environments: Web
status: Published
# AI-Q Premium Predictor Codelab: Understanding AI-Driven Job Displacement Insurance

This codelab provides a comprehensive guide to the AI-Q Premium Predictor, a Streamlit application designed to illustrate the factors influencing a hypothetical AI-driven job displacement insurance premium. This application is crucial for understanding how individuals can mitigate their risk in the face of increasing automation and technological advancements.

We'll walk through the application's architecture, key functionalities, and the underlying calculations. By the end of this codelab, you'll be able to:

*   Understand the core concepts of idiosyncratic and systematic risk.
*   Trace the calculation of the AI-Q premium from user inputs to the final monthly premium.
*   Identify the key factors influencing the premium and how proactive measures like upskilling can reduce it.
*   Appreciate the "Education is Insurance" paradigm.

## Application Overview
Duration: 00:05

The AI-Q Premium Predictor is built using Streamlit, a Python library for creating interactive web applications.  The application consists of three main files:

*   `app.py`: This is the main application file that defines the user interface, handles user inputs, performs calculations, and displays the results.
*   `application_pages/data_lookups.py`: This file contains static data, such as role multipliers, education level factors, and industry hazards, used in the premium calculation.  Essentially, it's a configuration file.
*   `application_pages/calculations.py`: This file contains the functions that perform the actual calculations of the various risk factors and the final premium.

The application's primary goal is to demonstrate how various personal, policy, and environmental factors contribute to the final insurance premium.  Users can interact with sliders and dropdowns to adjust these factors and see how they affect the calculated premium in real-time.

## Setting Up the Environment (Optional)
Duration: 00:02

While this codelab focuses on understanding the application's logic, running it locally requires Python and Streamlit.

1.  **Install Python:** Ensure you have Python 3.7 or higher installed.
2.  **Install Streamlit:** Open your terminal and run: `pip install streamlit`
3.  **Clone the Repository (if applicable):**  If the code is in a Git repository, clone it to your local machine.
4.  **Navigate to the Directory:**  Use the `cd` command to navigate to the directory containing the application files.
5.  **Run the Application:** Execute the following command in your terminal: `streamlit run app.py`

This will open the application in your web browser.

## Exploring `data_lookups.py`
Duration: 00:05

The `data_lookups.py` file stores static data used throughout the application. This includes factors for human capital, company risk, and base occupational hazards.

```python
import pandas as pd

# Data for Human Capital Factor (F_HC)
ROLE_MULTIPLIERS = {
    "Entry-level Analyst": 1.10,
    "Junior Specialist": 1.05,
    "Mid-level Professional": 1.00,
    "Senior Professional/Manager": 0.95,
    "Lead/Principal/Director": 0.90,
    "Executive/C-suite": 0.85,
    "Paralegal": 1.35, # Example from doc
    "Senior Research Scientist": 0.30 # Example from doc
}

EDUCATION_LEVEL_FACTORS = {
    "High School": 1.20,
    "Associate's Degree": 1.15,
    "Bachelor's Degree": 1.00,
    "Master's Degree": 0.90,
    "PhD/Doctorate": 0.80,
}

EDUCATION_FIELD_FACTORS = {
    "Liberal Arts/Humanities": 1.15,
    "Business/Management": 1.05,
    "Science/Research": 1.00,
    "Engineering/Computer Science/Quant": 0.90,
    "Healthcare/Medicine": 0.90,
}

SCHOOL_TIER_FACTORS = {
    "Tier 3 (Local/Regional)": 1.10,
    "Tier 2 (National/Reputable)": 1.00,
    "Tier 1 (Ivy/Top Global)": 0.90,
}

# Data for Company Risk Factor (F_CR)
COMPANY_RISK_FACTORS = {
    "Startup (High Risk)": 1.25,
    "Mid-size Firm (Medium Risk)": 1.00,
    "Big Firm (Lower Risk)": 0.85,
    "Government/Non-profit (Stable)": 0.75,
}

# Data for Base Occupational Hazard (H_base)
INDUSTRY_HAZARDS = {
    "Manufacturing (Automation Risk)": 80,
    "Retail (E-commerce Shift)": 75,
    "Transportation/Logistics (Autonomous Tech)": 70,
    "Customer Service (AI Bots)": 90,
    "Finance/Banking (Algorithmic Trading/AI)": 60,
    "IT/Software Development (Low-code/No-code/AI Dev)": 55,
    "Healthcare (AI Diagnostics/Robotics)": 45,
    "Education (Online Learning/AI Tutors)": 50,
    "Arts/Entertainment (AI Content Creation)": 65,
    "Legal (AI Legal Research)": 85,
}

# Default weights for F_CR and F_US in V_raw calculation
W_CR_DEFAULT = 0.4
W_US_DEFAULT = 0.6

# Default weights for M_econ and I_AI in H_i calculation
W_ECON_DEFAULT = 0.5
W_INNO_DEFAULT = 0.5

# Default gamma parameters for Upskilling Factor (F_US)
GAMMA_GEN_DEFAULT = 0.6 # portable skills are more rewarded
GAMMA_SPEC_DEFAULT = 0.4 # firm-specific skills are less rewarded
```

This file provides the lookup tables for different factors that are used to compute the insurance premium.  For example, `ROLE_MULTIPLIERS` provides a multiplier based on the job role, while `INDUSTRY_HAZARDS` defines the base occupational hazard for different industries. The `DEFAULT` variables store the weights and gamma parameters.

<aside class="positive">
These values are illustrative. In a real-world application, these factors would be derived from statistical analysis and actuarial science principles.
</aside>

## Understanding `calculations.py`: Idiosyncratic Risk
Duration: 00:15

The `calculations.py` file contains the core functions for calculating the various risk factors and the final premium.  Let's start with the Idiosyncratic Risk calculations.

```python
import math
from application_pages.data_lookups import (
    ROLE_MULTIPLIERS, EDUCATION_LEVEL_FACTORS, EDUCATION_FIELD_FACTORS,
    SCHOOL_TIER_FACTORS, COMPANY_RISK_FACTORS, INDUSTRY_HAZARDS,
    W_CR_DEFAULT, W_US_DEFAULT, W_ECON_DEFAULT, W_INNO_DEFAULT,
    GAMMA_GEN_DEFAULT, GAMMA_SPEC_DEFAULT
)

#  Idiosyncratic Risk (Vi(t)) Calculations 

def calculate_experience_factor(years_experience: float) -> float:
    """Calculates the Experience Factor (f_exp)."""
    return 1 - (0.015 * min(years_experience, 20.0))

def calculate_human_capital_factor(job_role: str, education_level: str, education_field: str, school_tier: str, years_experience: float) -> float:
    """Calculates the Human Capital Factor (F_HC)."""
    f_role = ROLE_MULTIPLIERS.get(job_role, 1.0)
    f_level = EDUCATION_LEVEL_FACTORS.get(education_level, 1.0)
    f_field = EDUCATION_FIELD_FACTORS.get(education_field, 1.0)
    f_school = SCHOOL_TIER_FACTORS.get(school_tier, 1.0)
    f_exp = calculate_experience_factor(years_experience)
    return f_role * f_level * f_field * f_school * f_exp

def calculate_company_risk_factor(company_type: str) -> float:
    """Retrieves the Company Risk Factor (F_CR) based on company type."""
    return COMPANY_RISK_FACTORS.get(company_type, 1.0)

def calculate_upskilling_factor(p_general_progress: float, p_specific_progress: float, gamma_gen: float = GAMMA_GEN_DEFAULT, gamma_spec: float = GAMMA_SPEC_DEFAULT) -> float:
    """Calculates the Upskilling Factor (F_US)."""
    p_gen_normalized = p_general_progress / 100.0
    p_spec_normalized = p_specific_progress / 100.0
    return 1 - (gamma_gen * p_gen_normalized + gamma_spec * p_spec_normalized)

def calculate_idiosyncratic_risk(f_hc: float, f_cr: float, f_us: float, w_cr: float = W_CR_DEFAULT, w_us: float = W_US_DEFAULT) -> float:
    """Calculates the final Idiosyncratic Risk score (Vi(t))."""
    v_raw = f_hc * (w_cr * f_cr + w_us * f_us)
    v_i = min(100.0, max(5.0, v_raw - 50.0))
    return v_i
```

1.  **`calculate_experience_factor`**: This function calculates an experience factor based on years of experience, with diminishing returns after 20 years.  It uses the formula `1 - (0.015 * min(years_experience, 20.0))`.
2.  **`calculate_human_capital_factor`**: This function computes the Human Capital Factor (`F_HC`) by multiplying several sub-factors:
    *   `f_role`: Based on the job role (using `ROLE_MULTIPLIERS` from `data_lookups.py`).
    *   `f_level`: Based on the education level (using `EDUCATION_LEVEL_FACTORS`).
    *   `f_field`: Based on the field of study (using `EDUCATION_FIELD_FACTORS`).
    *   `f_school`: Based on the school tier (using `SCHOOL_TIER_FACTORS`).
    *   `f_exp`: The experience factor calculated in the previous step.

    The formula is: `F_HC = f_role * f_level * f_field * f_school * f_exp`
3.  **`calculate_company_risk_factor`**: This function retrieves the Company Risk Factor (`F_CR`) based on the company type, using the `COMPANY_RISK_FACTORS` lookup table.
4.  **`calculate_upskilling_factor`**: This function calculates the Upskilling Factor (`F_US`) based on the progress in general and specific skills. The parameters `gamma_gen` and `gamma_spec` weight the contribution of general and specific skills, respectively. The formula is: `F_US = 1 - (gamma_gen * P_gen(t) + gamma_spec * P_spec(t))`
5.  **`calculate_idiosyncratic_risk`**:  This function calculates the final Idiosyncratic Risk score (`V_i(t)`) using the following steps:
    *   Calculates `V_raw`: a weighted average of the Company Risk Factor (`F_CR`) and the Upskilling Factor (`F_US`), multiplied by the Human Capital Factor (`F_HC`). The default weights for `F_CR` and `F_US` are 0.4 and 0.6, respectively.
    *   Normalizes `V_raw` to a range between 5.0 and 100.0.
    The Formula is:
        *   `V_raw = F_HC * (w_CR * F_CR + w_US * F_US)`
        *   `V_i(t) = min(100.0, max(5.0, V_raw - 50.0))`

## Understanding `calculations.py`: Systematic Risk
Duration: 00:10

Now, let's examine the Systematic Risk calculations.

```python
#  Systematic Risk (Hi) Calculations 

def calculate_base_occupational_hazard(
    current_industry: str,
    target_industry: str,
    months_elapsed_transition: int,
    ttv_period: int = 12 # Time-to-Value period, default 12 months
) -> float:
    """Calculates the Base Occupational Hazard (H_base(k))."""
    h_current = INDUSTRY_HAZARDS.get(current_industry, 50) # Default to 50 if not found
    h_target = INDUSTRY_HAZARDS.get(target_industry, 50) # Default to 50 if not found

    if months_elapsed_transition >= ttv_period:
        return float(h_target)
    elif months_elapsed_transition <= 0:
        return float(h_current)
    else:
        k = months_elapsed_transition
        ttv = float(ttv_period)
        return (1 - k/ttv) * h_current + (k/ttv) * h_target

def calculate_systematic_risk(
    h_base_t: float,
    m_econ: float,
    i_ai: float,
    w_econ: float = W_ECON_DEFAULT,
    w_inno: float = W_INNO_DEFAULT
) -> float:
    """Calculates the final Systematic Risk score (H_i)."""
    return h_base_t * (w_econ * m_econ + w_inno * i_ai)
```

1.  **`calculate_base_occupational_hazard`**: This function calculates the Base Occupational Hazard (`H_base(k)`) which is a weighted average of the hazard associated with the current industry and the target industry.  This allows modeling a career transition.
    *   `current_industry`: The industry the individual is currently in.
    *   `target_industry`: The industry the individual is transitioning to.
    *   `months_elapsed_transition`: The number of months since the start of the transition.
    *   `ttv_period`: The Time-To-Value period (default is 12 months).

    The formula is:
    *   `H_base(k) = (1 - k/TTV) * H_current + (k/TTV) * H_target`
    If `k >= TTV`, then `H_base(k) = H_target`.
    If `k <= 0`, then `H_base(k) = H_current`.
2.  **`calculate_systematic_risk`**: This function calculates the final Systematic Risk score (`H_i`) by combining the base occupational hazard with economic and AI innovation modifiers.
    *   `h_base_t`: The base occupational hazard calculated in the previous step.
    *   `m_econ`:  The economic climate modifier.
    *   `i_ai`: The AI innovation index.

    The formula is: `H_i = H_base(t) * (w_econ * M_econ + w_inno * I_AI)`

## Understanding `calculations.py`: Premium Determination
Duration: 00:10

The final section of `calculations.py` focuses on determining the insurance premium.

```python
#  Premium Determination Calculations 

def calculate_total_payout(
    annual_salary: float,
    coverage_percentage: float, # e.g., 25.0 for 25%
    coverage_duration_months: int
) -> float:
    """Calculates the Total Payout Amount (L_payout)."""
    return (annual_salary / 12.0) * coverage_duration_months * (coverage_percentage / 100.0)

def calculate_annual_claim_probability(
    h_i: float,
    v_i: float,
    beta_systemic: float,
    beta_individual: float
) -> float:
    """Calculates the Annual Claim Probability (P_claim)."""
    return (h_i / 100.0 * beta_systemic) * (v_i / 100.0 * beta_individual)

def calculate_expected_loss(p_claim: float, l_payout: float) -> float:
    """Calculates the Annual Expected Loss (E[Loss])."""
    return p_claim * l_payout

def calculate_final_monthly_premium(
    e_loss: float,
    lambda_factor: float,
    p_min: float
) -> float:
    """Calculates the Final Monthly Premium (P_monthly)."""
    return max((e_loss * lambda_factor) / 12.0, p_min)
```

1.  **`calculate_total_payout`**: This function calculates the total payout amount (`L_payout`) based on the annual salary, coverage percentage, and coverage duration.
    The formula is: `L_payout = (Annual Salary / 12) * Coverage Duration * (Coverage Percentage / 100)`
2.  **`calculate_annual_claim_probability`**: This function calculates the annual claim probability (`P_claim`) based on the systematic risk, idiosyncratic risk, and two calibrated parameters, `beta_systemic` and `beta_individual`.
    The formula is: `P_claim = (H_i / 100 * beta_systemic) * (V_i(t) / 100 * beta_individual)`
3.  **`calculate_expected_loss`**: This function calculates the annual expected loss (`E[Loss]`) by multiplying the annual claim probability by the total payout amount.
    The formula is: `E[Loss] = P_claim * L_payout`
4.  **`calculate_final_monthly_premium`**: This function calculates the final monthly premium (`P_monthly`) by dividing the annual expected loss (adjusted by a loading factor `lambda_factor`) by 12, and taking the maximum of this value and a minimum premium `p_min`.
    The formula is: `P_monthly = max((E[Loss] * lambda_factor) / 12, p_min)`

## Exploring `app.py`: User Interface and Logic
Duration: 00:20

Now, let's examine the `app.py` file, which defines the user interface and orchestrates the calculations.

