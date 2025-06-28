
import pandas as pd

# Data for Human Capital Factor (F_HC)
# These are illustrative multipliers. Actual values would be derived from statistical analysis.
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

# Experience factor: 1 - (0.015 * min(Yrs, 20))
# This is a function, not a lookup table, handled in calculation.py

# Data for Company Risk Factor (F_CR)
# These are illustrative scores for different company types.
# In a real system, these would be dynamic scores (S_senti, S_fin, S_growth)
COMPANY_RISK_FACTORS = {
    "Startup (High Risk)": 1.25,
    "Mid-size Firm (Medium Risk)": 1.00,
    "Big Firm (Lower Risk)": 0.85,
    "Government/Non-profit (Stable)": 0.75,
}

# Data for Base Occupational Hazard (H_base)
# These are illustrative base hazard scores for different industries.
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
