
import math
from application_pages.data_lookups import (
    ROLE_MULTIPLIERS, EDUCATION_LEVEL_FACTORS, EDUCATION_FIELD_FACTORS,
    SCHOOL_TIER_FACTORS, COMPANY_RISK_FACTORS, INDUSTRY_HAZARDS,
    W_CR_DEFAULT, W_US_DEFAULT, W_ECON_DEFAULT, W_INNO_DEFAULT,
    GAMMA_GEN_DEFAULT, GAMMA_SPEC_DEFAULT
)

# --- Idiosyncratic Risk (Vi(t)) Calculations ---

def calculate_experience_factor(years_experience: float) -> float:
    """
    Calculates the Experience Factor (f_exp).
    f_exp: Experience Factor, typically a decaying function like 1 - (0.015 * min(Yrs, 20)).
    """
    return 1 - (0.015 * min(years_experience, 20.0))

def calculate_human_capital_factor(
    job_role: str,
    education_level: str,
    education_field: str,
    school_tier: str,
    years_experience: float
) -> float:
    """
    Calculates the Human Capital Factor (F_HC).
    F_HC = f_role * f_level * f_field * f_school * f_exp
    """
    f_role = ROLE_MULTIPLIERS.get(job_role, 1.0)
    f_level = EDUCATION_LEVEL_FACTORS.get(education_level, 1.0)
    f_field = EDUCATION_FIELD_FACTORS.get(education_field, 1.0)
    f_school = SCHOOL_TIER_FACTORS.get(school_tier, 1.0)
    f_exp = calculate_experience_factor(years_experience)
    return f_role * f_level * f_field * f_school * f_exp

def calculate_company_risk_factor(company_type: str) -> float:
    """
    Retrieves the Company Risk Factor (F_CR) based on company type.
    """
    return COMPANY_RISK_FACTORS.get(company_type, 1.0)

def calculate_upskilling_factor(
    p_general_progress: float,
    p_specific_progress: float,
    gamma_gen: float = GAMMA_GEN_DEFAULT,
    gamma_spec: float = GAMMA_SPEC_DEFAULT
) -> float:
    """
    Calculates the Upskilling Factor (F_US).
    F_US = 1 - (gamma_gen * P_gen(t) + gamma_spec * P_spec(t))
    P_gen(t) and P_spec(t) are progress from 0 to 1 (or 0-100%).
    """
    p_gen_normalized = p_general_progress / 100.0
    p_spec_normalized = p_specific_progress / 100.0
    return 1 - (gamma_gen * p_gen_normalized + gamma_spec * p_spec_normalized)

def calculate_idiosyncratic_risk(
    f_hc: float,
    f_cr: float,
    f_us: float,
    w_cr: float = W_CR_DEFAULT,
    w_us: float = W_US_DEFAULT
) -> float:
    """
    Calculates the final Idiosyncratic Risk score (Vi(t)).
    V_raw = F_HC * (w_CR * F_CR + w_US * F_US)
    V_i(t) = min(100.0, max(5.0, V_raw - 50.0))
    """
    v_raw = f_hc * (w_cr * f_cr + w_us * f_us)
    v_i = min(100.0, max(5.0, v_raw - 50.0))
    return v_i

# --- Systematic Risk (Hi) Calculations ---

def calculate_base_occupational_hazard(
    current_industry: str,
    target_industry: str,
    months_elapsed_transition: int,
    ttv_period: int = 12 # Time-to-Value period, default 12 months
) -> float:
    """
    Calculates the Base Occupational Hazard (H_base(k)).
    H_base(k) = (1 - k/TTV) * H_current + (k/TTV) * H_target
    If k >= TTV, it's fully H_target. If k == 0, it's H_current.
    """
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
    """
    Calculates the final Systematic Risk score (H_i).
    H_i = H_base(t) * (w_econ * M_econ + w_inno * I_AI)
    """
    return h_base_t * (w_econ * m_econ + w_inno * i_ai)

# --- Premium Determination Calculations ---

def calculate_total_payout(
    annual_salary: float,
    coverage_percentage: float, # e.g., 25.0 for 25%
    coverage_duration_months: int
) -> float:
    """
    Calculates the Total Payout Amount (L_payout).
    L_payout = (Annual Salary / 12) * Coverage Duration * Coverage Percentage
    """
    return (annual_salary / 12.0) * coverage_duration_months * (coverage_percentage / 100.0)

def calculate_annual_claim_probability(
    h_i: float,
    v_i: float,
    beta_systemic: float,
    beta_individual: float
) -> float:
    """
    Calculates the Annual Claim Probability (P_claim).
    P_claim = (H_i / 100 * beta_systemic) * (V_i(t) / 100 * beta_individual)
    """
    return (h_i / 100.0 * beta_systemic) * (v_i / 100.0 * beta_individual)

def calculate_expected_loss(p_claim: float, l_payout: float) -> float:
    """
    Calculates the Annual Expected Loss (E[Loss]).
    E[Loss] = P_claim * L_payout
    """
    return p_claim * l_payout

def calculate_final_monthly_premium(
    e_loss: float,
    lambda_factor: float,
    p_min: float
) -> float:
    """
    Calculates the Final Monthly Premium (P_monthly).
    P_monthly = max((E[Loss] * lambda) / 12, P_min)
    """
    return max((e_loss * lambda_factor) / 12.0, p_min)
