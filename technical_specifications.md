
# Technical Specifications for AI-Q Premium Predictor Streamlit Application

## Overview

The AI-Q Premium Predictor is an interactive Streamlit application designed to help users understand and estimate a hypothetical AI-driven job displacement insurance premium. It operationalizes the actuarial model outlined in the accompanying document, specifically focusing on the 'Risk Computation and Premium Determination' section (Section 4). The application will allow users to input various personal and policy parameters, visualize the step-by-step calculation of their risk profile, annual claim probability, expected loss, and ultimately, their final monthly premium. This interactive approach aims to demystify complex financial concepts and illustrate the "Education is Insurance" paradigm by demonstrating how proactive risk mitigation efforts can lead to lower premiums.

## Step-by-Step Development Process

The development of the AI-Q Premium Predictor application will follow a modular and iterative approach:

1.  **Project Setup and Environment Initialization:**
    *   Create a new Python virtual environment.
    *   Install core libraries: `streamlit`, `pandas`, `plotly`.
    *   Initialize the main application file (e.g., `app.py`).

2.  **Data Loading and Static Lookups:**
    *   Define Python dictionaries or Pandas DataFrames to store static lookup values for risk factors (e.g., `f_role`, `f_level`, `f_field`, `f_school` multipliers, `H_base` for industries, `F_CR` for company types). These will mimic the "synthetic dataset" for initial values.
    *   Implement functions to retrieve these values based on user selections.

3.  **User Interface (UI) - Input Forms:**
    *   Design Streamlit sidebar for core inputs:
        *   **Personal Risk Factors (Idiosyncratic Risk):** Sliders, dropdowns, or number inputs for education level, field, school tier, years of experience, current job role, company type, and upskilling progress (general vs. firm-specific).
        *   **Policy Parameters:** Number inputs for Annual Salary, Coverage Percentage, Coverage Duration, Systemic Event Base Probability ($\beta_{systemic}$), Individual Loss Base Probability ($\beta_{individual}$), Loading Factor ($\lambda$), and Minimum Premium ($P_{min}$).
        *   **Systematic Risk Factors:** Sliders or dropdowns for economic climate (e.g., represented as a multiplier for `M_econ`) and AI innovation index (e.g., represented as a multiplier for `I_AI`).
        *   **Career Transition:** Inputs for target industry and elapsed months since transition (for `H_base(t)` calculation).
    *   Implement `st.sidebar` for cleaner organization.

4.  **Core Calculation Logic - Mathematical Modules:**
    *   Develop Python functions for each mathematical formula, ensuring correct order of operations and variable handling.
    *   **Idiosyncratic Risk ($V_i(t)$) Calculation:**
        *   `calculate_human_capital_factor(f_role, f_level, f_field, f_school, f_exp)`
        *   `calculate_company_risk_factor(company_type)` (lookup)
        *   `calculate_upskilling_factor(p_general, p_specific, y_general, y_specific)`
        *   `calculate_idiosyncratic_risk(F_HC, F_CR, F_US, w_CR, w_US)`
    *   **Systematic Risk ($H_i$) Calculation:**
        *   `calculate_base_occupational_hazard(current_industry_H, target_industry_H, k_months, ttv_period)`
        *   `calculate_environmental_modifiers(m_econ_input, i_ai_input)`
        *   `calculate_systematic_risk(H_base_t, m_econ, i_ai, w_econ, w_inno)`
    *   **Premium Determination:**
        *   `calculate_annual_claim_probability(H_i, V_i, beta_systemic, beta_individual)`
        *   `calculate_total_payout(annual_salary, coverage_percentage, coverage_duration_months)`
        *   `calculate_expected_loss(P_claim, L_payout)`
        *   `calculate_final_monthly_premium(E_Loss, lambda_factor, P_min)`

5.  **Interactive Display and Visualizations:**
    *   Display intermediate calculation results in an organized manner using `st.expander` or `st.tabs` for clarity.
    *   Generate interactive charts using `plotly.express` or `plotly.graph_objects`:
        *   A gauge chart or bar chart for the `Final Monthly Premium`.
        *   Potentially, bar charts to show contributions of `F_HC`, `F_CR`, `F_US` to `V_i(t)` or a breakdown of `H_i` components.
        *   If a time-series element is introduced (e.g., showing `H_base(t)` evolution over `k` months), a line chart.
    *   Add annotations and tooltips using Streamlit's `st.help` or custom `st.info` messages for inputs and outputs.

6.  **Documentation and Explanations:**
    *   Integrate markdown `st.markdown` for concept definitions, formula explanations, and real-world applications within the main content area.
    *   Ensure all mathematical formulae adhere to the specified LaTeX formatting rules.
    *   Reference relevant sections of the document (`Section 4`, `Section C.3.1`, `Section 4.2.1`, `Section 4.2.2`, `Section 4.1`).

7.  **Refinement and Testing:**
    *   Test all input combinations to ensure calculations are correct and visualizations update dynamically.
    *   Refine UI layout and explanations for clarity and user-friendliness.

## Core Concepts and Mathematical Foundations

The application is built upon several interconnected mathematical concepts from the document, which are explained and calculated as follows:

### Idiosyncratic Risk ($V_i(t)$)
The Idiosyncratic Risk, or Vulnerability, is a multi-factor assessment of an individual's specific vulnerability to job displacement. It is calculated as a composite of the Human Capital Factor ($F_{HC}$), Company Risk Factor ($F_{CR}$), and Upskilling Factor ($F_{US}$), then normalized.

The document defines a general form:
$$
V_i(t) = f(F_{HC}, F_{CR}, F_{US})
$$
And specifies it as a weighted product for the raw score ($V_{raw}$):
$$
V_{raw} = F_{HC} \cdot (w_{CR} \cdot F_{CR} + w_{US} \cdot F_{US})
$$
The final $V_i(t)$ is normalized:
$$
V_i(t) = \min(100.0, \max(5.0, V_{raw} - 50.0))
$$
Where:
- $V_i(t)$: Final Idiosyncratic Risk score (0-100 scale).
- $F_{HC}$: Human Capital Factor.
- $F_{CR}$: Company Risk Factor.
- $F_{US}$: Upskilling Factor.
- $w_{CR}$: Weight for Company Risk Factor (e.g., 0.4 from document's example).
- $w_{US}$: Weight for Upskilling Factor (e.g., 0.6 from document's example).

This formula quantifies how an individual's personal attributes and actions (like upskilling) contribute to their unique risk profile.

#### Human Capital Factor ($F_{HC}$)
The Human Capital Factor assesses an individual's foundational resilience based on their educational and professional background. It is calculated as a weighted product of several sub-factors:
$$
F_{HC} = f_{role} \cdot f_{level} \cdot f_{field} \cdot f_{school} \cdot f_{exp}
$$
Where:
- $f_{role}$: Role Multiplier (e.g., based on job title vulnerability).
- $f_{level}$: Education Level Factor (e.g., PhD vs. Bachelor's).
- $f_{field}$: Education Field Factor (e.g., Tech vs. Liberal Arts).
- $f_{school}$: Institution Tier Factor (e.g., Tier 1 vs. Tier 3 university).
- $f_{exp}$: Experience Factor, typically a decaying function like $1 - (0.015 \cdot \min(Yrs, 20))$, where $Yrs$ are years of experience.

This factor reflects an individual's inherent strengths and vulnerabilities based on their professional history and academic background.

#### Company Risk Factor ($F_{CR}$)
The Company Risk Factor quantifies the stability and growth prospects of the individual's current employer, analogous to a corporate credit rating. It is calculated using:
$$
F_{CR} = w_1 \cdot S_{senti} + w_2 \cdot S_{fin} + w_3 \cdot S_{growth}
$$
Where:
- $S_{senti}$: Sentiment Score (e.g., from real-time NLP analysis of news).
- $S_{fin}$: Financial Health Score (e.g., from financial statements).
- $S_{growth}$: Growth & AI-Adoption Score (e.g., R&D spending, hiring trends).
- $w_1, w_2, w_3$: Weights for each sub-factor.

This factor accounts for the stability of the employer as a component of an individual's risk.

#### Upskilling Factor ($F_{US}$)
The Upskilling Factor differentiates between skill types, rewarding portable skills more heavily. It is defined as:
$$
F_{US} = 1 - (\gamma_{gen} \cdot P_{gen}(t) + \gamma_{spec} \cdot P_{spec}(t))
$$
Where:
- $P_{gen}(t)$: Individual's training progress (from 0 to 1) in "General" or "Portable" skills (e.g., Python).
- $P_{spec}(t)$: Individual's training progress (from 0 to 1) in "Firm-Specific" skills (e.g., proprietary software).
- $\gamma_{gen}, \gamma_{spec}$: Weighting parameters ensuring $\gamma_{gen} > \gamma_{spec}$.

This factor quantifies the reduction in idiosyncratic risk due to an individual's proactive learning efforts.

### Systematic Risk ($H_i$)
The Systematic Risk score is a dynamic index reflecting the occupational hazard and the broader environment. It is calculated as the Base Occupational Hazard, adjusted by two environmental modifiers:
$$
H_i = H_{base}(t) \cdot (w_{econ} \cdot M_{econ} + w_{inno} \cdot I_{AI})
$$
Where:
- $H_i$: Final Systematic Risk score (0-100 scale).
- $H_{base}(t)$: Base Occupational Hazard for an occupation.
- $M_{econ}$: Economic Climate Modifier.
- $I_{AI}$: AI Innovation Index.
- $w_{econ}, w_{inno}$: Calibration weights that sum to 1.0 (e.g., 0.5 each).

This score accounts for macro-level risks inherent to an occupation, influenced by economic conditions and AI advancements.

#### Base Occupational Hazard ($H_{base}(t)$)
The foundational occupational hazard score, which can change over time based on the user's actions (e.g., career transition). Upon completion of a "Transition Pathway," the individual's $H_{base}$ does not instantly switch to the target industry's score. Instead, for a defined "TTV Period" (e.g., 12 months), the score is a time-weighted average of the old and new industry risks:
$$
H_{base}(k) = \left(1 - \frac{k}{TTV}\right) \cdot H_{current} + \left(\frac{k}{TTV}\right) \cdot H_{target}
$$
Where:
- $k$: Number of months elapsed since completion of transition pathway.
- $TTV$: Total number of months in the Time-to-Value period (e.g., 12).
- $H_{current}$: Base Occupational Hazard of the individual's original industry.
- $H_{target}$: Base Occupational Hazard of the new target industry.

This formula demonstrates how systematic risk evolves during a career transition.

#### Environmental Modifiers ($M_{econ}$, $I_{AI}$)
The model incorporates an 'Economic Climate Modifier' ($M_{econ}$) and an 'AI Innovation Index' ($I_{AI}$) to dynamically adjust risk based on real-time macro trends.
- $M_{econ}$: A composite index (e.g., from 0.8 to 1.2) derived from factors like GDP Growth, Sector Employment, and Interest Rates. A recessionary climate may temporarily slow displacement risk.
- $I_{AI}$: A momentum indicator capturing the velocity of AI development and adoption, derived from factors including VC Funding, R&D Spend, and Public Salience. A period of rapid breakthroughs can accelerate displacement risk.

These modifiers dynamically adjust the systematic risk based on the external economic and technological environment.

### Total Payout Amount ($L_{payout}$)
The total amount that would be paid out if a claim is triggered, defined by the policy terms.
$$
L_{payout} = \frac{Annual\ Salary}{12} \cdot Coverage\ Duration \cdot Coverage\ Percentage
$$
Where:
- $Annual\ Salary$: User's annual salary input.
- $Coverage\ Duration$: Duration of coverage in months (e.g., 6 months).
- $Coverage\ Percentage$: Percentage of income covered (e.g., 25%).

This calculation determines the financial benefit received in case of a valid claim.

### Annual Claim Probability ($P_{claim}$)
The annual probability of a claim is modeled as the joint probability of a systemic event occurring and that event leading to a loss for that specific individual. It is directly calculated from the final Idiosyncratic Risk ($V_i(t)$) and Systematic Risk ($H_i$) scores, along with base probabilities.
$$
P_{claim} = \left(\frac{H_i}{100} \cdot \beta_{systemic}\right) \cdot \left(\frac{V_i(t)}{100} \cdot \beta_{individual}\right)
$$
Where:
- $H_i$: Final Systematic Risk score.
- $V_i(t)$: Final Idiosyncratic Risk score.
- $\beta_{systemic}$: Systemic Event Base Probability (e.g., 0.10), a calibrated actuarial parameter for a systemic displacement event in the highest-risk industry.
- $\beta_{individual}$: Individual Loss Base Probability (e.g., 0.50), a calibrated parameter for job loss for the most vulnerable person given a systemic event.

This formula calculates the likelihood of a job displacement event occurring for the individual within a year.

### Annual Expected Loss ($E[\text{Loss}]$)
The expected loss is the total payout amount multiplied by the probability of a claim.
$$
E[\text{Loss}] = P_{claim} \cdot L_{payout}
$$
Where:
- $P_{claim}$: Annual Claim Probability.
- $L_{payout}$: Total Payout Amount.

This value represents the average financial loss expected over a year, given the calculated risk.

### Final Monthly Premium ($P_{monthly}$)
The final monthly premium is determined by adjusting the annual expected loss by a loading factor and ensuring it meets a minimum premium threshold.
$$
P_{monthly} = \max\left(\frac{E[\text{Loss}] \cdot \lambda}{12}, P_{min}\right)
$$
Where:
- $E[\text{Loss}]$: Annual Expected Loss.
- $\lambda$: Loading Factor (e.g., 1.5), a standard insurance multiplier to cover administrative costs, operational expenses, and profit margin.
- $P_{min}$: Minimum Premium (e.g., $20.00), a floor on the monthly premium to ensure policy viability.

This formula represents the final cost to the user for the hypothetical AI-driven job displacement insurance.

## Required Libraries and Dependencies

The application will primarily rely on the following Python libraries:

*   **`streamlit`**:
    *   **Version**: Latest stable release (e.g., `^1.29.0`).
    *   **Specific functions/modules**:
        *   `st.sidebar`: For organizing input widgets.
        *   `st.header`, `st.subheader`, `st.markdown`: For structuring content and displaying explanations.
        *   `st.number_input`, `st.slider`, `st.selectbox`, `st.radio`: For various user input widgets to configure parameters.
        *   `st.metric`: For displaying key performance indicators like the final premium.
        *   `st.expander`: For organizing sections of detailed calculations.
        *   `st.pyplot` (indirectly via `matplotlib` if used) or `st.plotly_chart`: For embedding interactive visualizations.
        *   `st.info`, `st.help`: For inline documentation and tooltips.
    *   **Role**: Core framework for building the web application, handling UI rendering, interactivity, and data flow.
    *   **Usage Example**:
        ```python
        import streamlit as st
        st.sidebar.header("User Inputs")
        annual_salary = st.sidebar.number_input("Annual Salary", value=90000.0, min_value=0.0)
        st.markdown("### Final Monthly Premium")
        st.metric(label="Premium", value=f"${premium:.2f}")
        ```

*   **`pandas`**:
    *   **Version**: Latest stable release (e.g., `^2.1.3`).
    *   **Specific functions/modules**: `pd.DataFrame`, `pd.Series`.
    *   **Role**: Data handling for static lookup tables (e.g., `f_role` multipliers, `H_base` values for industries, `F_CR` values for company types). While the dataset is synthetic and small, `pandas` provides a robust way to manage these lookups.
    *   **Usage Example**:
        ```python
        import pandas as pd
        role_multipliers = pd.DataFrame({
            'Job Role': ['Paralegal', 'Senior Research Scientist'],
            'Multiplier': [1.35, 0.30]
        }).set_index('Job Role')
        f_role_value = role_multipliers.loc[selected_role, 'Multiplier']
        ```

*   **`plotly` (and `plotly.express`)**:
    *   **Version**: Latest stable release (e.g., `^5.18.0`).
    *   **Specific functions/modules**: `plotly.graph_objects` (for gauge charts), `plotly.express` (for simpler charts like bar/line if needed).
    *   **Role**: Creating interactive data visualizations to display results like the monthly premium and component breakdowns.
    *   **Usage Example**:
        ```python
        import plotly.graph_objects as go
        fig = go.Figure(go.Indicator(
            mode = "gauge+number",
            value = monthly_premium,
            title = {'text': "Calculated Monthly Premium"},
            gauge = {'axis': {'range': [None, 100]},
                     'steps': [
                         {'range': [0, 20], 'color': "lightgreen"},
                         {'range': [20, 50], 'color': "lightyellow"},
                         {'range': [50, 100], 'color': "lightcoral"}],
                     'threshold' : {'line': {'color': "red", 'width': 4}, 'thickness': 0.75, 'value': 75}}))
        st.plotly_chart(fig, use_container_width=True)
        ```

## Implementation Details

The application's internal structure will follow a clear separation of concerns:

1.  **`app.py` (Main Application File):**
    *   Initializes Streamlit page configuration.
    *   Contains the main layout, including sidebar inputs and main content area.
    *   Calls functions from `calculations.py` and `data_lookups.py`.
    *   Renders markdown explanations and charts.
    *   Handles user session state if needed for complex interactions or multi-step processes, although for this predictor, direct calculation based on current inputs is sufficient.

2.  **`data_lookups.py` (Data Module):**
    *   Houses dictionaries or Pandas DataFrames for all static lookup values specified in the document (e.g., multipliers for `f_role`, `f_level`, `f_field`, `f_school`, `f_exp`, `F_CR` for company types, `H_base` for industries).
    *   Provides simple functions to retrieve values based on input keys.
    *   This module represents the "synthetic dataset" mentioned in the requirements, providing structured data for calculations.

3.  **`calculations.py` (Logic Module):**
    *   Contains all the Python functions implementing the mathematical formulae outlined in "Core Concepts and Mathematical Foundations".
    *   Each formula will have its own dedicated function, taking relevant parameters as arguments and returning the calculated value.
    *   Functions will be designed to be pure (i.e., given the same inputs, they always return the same output, with no side effects).
    *   Example structure:
        ```python
        def calculate_human_capital_factor(role_mult, level_mult, field_mult, school_mult, exp_mult):
            return role_mult * level_mult * field_mult * school_mult * exp_mult

        def calculate_idiosyncratic_risk(F_HC, F_CR, F_US, w_CR=0.4, w_US=0.6):
            V_raw = F_HC * (w_CR * F_CR + w_US * F_US)
            V_i = min(100.0, max(5.0, V_raw - 50.0))
            return V_i
        ```

## User Interface Components

The user interface will be designed for clarity, interactivity, and ease of understanding, following the principles of the "AI-Q Score Pricing Engine" and Section C.3.1.

*   **Sidebar (Input Configuration):**
    *   **Personal Profile:**
        *   `st.selectbox` or `st.radio` for "Job Role" (e.g., Paralegal, Senior Research Scientist).
        *   `st.slider` for "Years of Experience" (0-30).
        *   `st.selectbox` for "Education Level" (e.g., PhD, Master's, Bachelor's, High School).
        *   `st.selectbox` for "Education Field" (e.g., Tech/Engineering/Quant, Liberal Arts/Humanities).
        *   `st.selectbox` for "School Tier" (Tier 1, Tier 2, Tier 3).
        *   `st.selectbox` for "Company Type" (e.g., Big firm, Mid-size firm, Startup).
        *   `st.slider` for "General Skills Upskilling Progress" (0-100%).
        *   `st.slider` for "Firm-Specific Skills Upskilling Progress" (0-100%).
    *   **Policy Parameters (Section C.3.1):**
        *   `st.number_input` for "Annual Salary".
        *   `st.slider` for "Coverage Percentage" (e.g., 10-50%).
        *   `st.slider` for "Coverage Duration (Months)" (e.g., 3-12 months).
        *   `st.number_input` for "Systemic Event Base Probability ($\beta_{systemic}$)" (e.g., 0.10).
        *   `st.number_input` for "Individual Loss Base Probability ($\beta_{individual}$)" (e.g., 0.50).
        *   `st.number_input` for "Loading Factor ($\lambda$)" (e.g., 1.5).
        *   `st.number_input` for "Minimum Premium ($P_{min}$)" (e.g., 20.00).
    *   **Environmental Factors & Career Transition:**
        *   `st.slider` for "Economic Climate Modifier" (e.g., 0.8 to 1.2).
        *   `st.slider` for "AI Innovation Index" (e.g., 0.8 to 1.2).
        *   `st.selectbox` for "Current Industry" and "Target Industry".
        *   `st.slider` for "Months Elapsed Since Transition" (`k`).

*   **Main Content Area (Output and Explanations):**
    *   **Overview and Introduction:** `st.markdown` to introduce the application and its purpose, linking to the "AI-Q Score Pricing Engine" concept (Section 4.1).
    *   **Step-by-Step Calculation Flow:**
        *   Use `st.expander` or `st.tabs` for each major calculation step:
            *   **Idiosyncratic Risk ($V_i(t)$) Details:** Display calculated `F_HC`, `F_CR`, `F_US`, `V_raw`, and final `V_i(t)`. Include `st.info` or `st.help` for definitions of each sub-factor.
            *   **Systematic Risk ($H_i$) Details:** Display calculated `H_{base}(t)`, `M_{econ}`, `I_{AI}`, and final `H_i`. Include `st.info` or `st.help` for definitions.
            *   **Claim & Loss Calculation:** Display `L_{payout}`, `P_{claim}`, and `E[Loss]`.
            *   **Final Premium:** Clearly show the `P_{monthly}`.
        *   Each step will be accompanied by markdown explanations of the concepts and the corresponding LaTeX formula.
    *   **Interactive Charts:**
        *   A prominent `plotly` gauge chart for `P_{monthly}`.
        *   Potentially a bar chart showing the relative contribution of `E[Loss]` and `P_{min}` to the final premium if `P_{min}` is the binding constraint.
    *   **Contextual Explanations:** Extensive `st.markdown` sections providing definitions, practical examples, and real-world applications for each concept, directly referencing the document's content (e.g., Section 4.2.1 for `P_claim`, Section 4.2.2 for `P_monthly`).
    *   **"Education is Insurance" Paradigm:** A dedicated section explaining how changes in inputs (e.g., upskilling progress, career transition) directly impact the calculated premium, reinforcing the core idea from the document.


### Appendix Code

```code
Vi(t) = f (FHC, FCR, FUS)
Vraw = FHC * (WCR * FCR + WUS * FUS)
FHC = frole * flevel * ffield * fschool * fexp
FCR = W1 * Ssenti + W2 * Sfin + W3 * Sgrowth
FUS = 1 - (ygen * Pgen(t) + Yspec * Pspec(t))
Hi = Hbase(t) * (Wecon * Mecon + Winno * IAI)
Hbase(k) = (1 - k / TTV) * Hcurrent + (k / TTV) * Htarget
Mecon = f(GDP Growth, Sector Employment, Interest Rates)
IAI = f(VC Funding, R&D Spend, Public Salience)
Pclaim = Psystemic * Pindividual_systemic
Psystemic = Hi / 100 * Bsystemic
Pindividual_systemic = Vi(t) / 100 * Bindividual
Pmonthly = max (E[Loss] * λ / 12, Pmin)

# Step-by-Step Calculation Formulas and Values (derived from document examples)

# For Human Capital Factor (FHC)
# PRODUCT (FHC) = frole * fievel * ffield * fschool * fexp
# Persona A (Alex): 1.35 * 1.00 * 1.10 * 1.00 * 0.85 = 1.262
# Persona B (Brenda): 0.3 * 0.85 * 0.90 * 0.95 * 0.88 = 0.192

# For Idiosyncratic Risk (Vi(t))
# Weights: WCR = 0.4, wus = 0.6
# Raw Score: Vraw = FHC * (WCR * FCR + WUS * FUS)
# Final Score: Vi(t) = min(100.0, max(5.0, Vraw * 50.0))

# Initial Calculation (Persona A & B, Training Progress = 0%, FUS = 1.0)
# Persona A (Alex Chen, Paralegal):
# FHC = 1.262
# FCR = 0.95 (from lookup 'Big firm')
# FUS = 1 - (0.7 * 0.0) = 1.0
# Vraw = 1.262 * (0.4 * 0.95 + 0.6 * 1.0) = 1.262 * (0.38 + 0.6) = 1.262 * 0.98 = 1.23676 (approx 1.237 as per doc)
# Vi(t) = min(100.0, max(5.0, 1.237 * 50.0)) = min(100.0, max(5.0, 61.85)) = 61.85

# Persona B (Dr. Brenda Smith, Research Scientist):
# FHC = 0.192
# FCR = 1.00 (from lookup 'Mid-size firm')
# FUS = 1 - (0.7 * 0.0) = 1.0
# Vraw = 0.192 * (0.4 * 1.00 + 0.6 * 1.0) = 0.192 * (0.4 + 0.6) = 0.192 * 1.0 = 0.192
# Vi(t) = min(100.0, max(5.0, 0.192 * 50.0)) = min(100.0, max(5.0, 9.6)) = 9.6

# Illustrating Impact of Upskilling (Alex Chen, Pidio = 0.5)
# New FUS = 1 - (0.7 * 0.5) = 1 - 0.35 = 0.65
# New Vraw = 1.262 * (0.4 * 0.95 + 0.6 * 0.65) = 1.262 * (0.38 + 0.39) = 1.262 * 0.77 = 0.97174 (approx 0.972 as per doc)
# New Final Score = min(100.0, max(5.0, 0.972 * 50.0)) = min(100.0, max(5.0, 48.6)) = 48.6

# For Systematic Risk (Hi)
# Weights: Wecon = 0.5, Winno = 0.5

# Initial State Calculation (Neutral Economic & Innovation Environment: Mecon = 1.0, IAI = 1.0)
# Persona A (Alex Chen, Legal Industry Hcurrent = 65):
# Hi = Hbase(t) * (Wecon * Mecon + Winno * IAI)
# Hi = 65 * (0.5 * 1.0 + 0.5 * 1.0) = 65 * (0.5 + 0.5) = 65 * 1.0 = 65.0

# Persona B (Dr. Brenda Smith, Healthcare & Life Sciences Industry Hcurrent = 30):
# Hi = 30 * (0.5 * 1.0 + 0.5 * 1.0) = 30 * 1.0 = 30.0

# Illustrating Impact of Career Path Diversification (Alex Chen target Htarget = 30, TTV = 12 months)
# Scenario A: 6 Months After Pathway Completion (k = 6)
# New Hbase(t) = (1 - 6/12) * 65 + (6/12) * 30 = (0.5) * 65 + (0.5) * 30 = 32.5 + 15 = 47.5
# New Final Score (Hi) = 47.5 * (1.0) = 47.5 (Assuming environmental modifiers are still 1.0)

# Scenario B: 13 Months After Pathway Completion (k > 12)
# New Hbase(t) = 30 (Since TTV period is complete, Hbase = Htarget)
# New Final Score (Hi) = 30 * (1.0) = 30.0 (Assuming environmental modifiers are still 1.0)

# For Premium Determination
# C.3.1 Parameters:
# Annual Salary: $90,000
# Coverage Percentage: 25%
# Coverage Duration: 6 months
# Systemic Event Base Probability (Bsystemic): 0.10
# Individual Loss Base Probability (Bindividual): 0.50
# Loading Factor (λ): 1.5
# Minimum Premium (Pmin): $20.00

# C.3.2 Calculate Total Payout Amount (Lpayout):
# Lpayout = (Annual Salary / 12) * Coverage Duration * Coverage Percentage
# Calculation (as per doc): ($90,000 / 12) * 6 * 0.25 = $7,500.00
# Note: The document then states "$7,500 * 1.5 = $11,250" and uses $11,250 as Lpayout in subsequent steps, despite the formula for Lpayout not including lambda.
# For consistency with the document's calculations, we will use Lpayout = $11,250 for subsequent steps.

# C.3.3 Calculate Annual Claim Probability (Pclaim):
# Pclaim = (Hi / 100 * Bsystemic) * (Vi / 100 * Bindividual)
# Persona A (Alex Chen):
# Pclaim = (65.0 / 100 * 0.10) * (61.8 / 100 * 0.50) = (0.065) * (0.30925) = 0.0201 (or 2.01%)
# Persona B (Dr. Brenda Smith):
# Pclaim = (30.0 / 100 * 0.10) * (9.6 / 100 * 0.50) = (0.03) * (0.048) = 0.00144 (or 0.144%)

# C.3.4 Calculate Annual Expected Loss (E[Loss]):
# E[Loss] = Pclaim * Lpayout
# Persona A (Alex Chen): E[Loss] = 0.0201 * $11,250 = $226.13
# Persona B (Dr. Brenda Smith): E[Loss] = 0.00144 * $11,250 = $16.20

# C.3.5 Calculate Final Monthly Premium (Pmonthly):
# Pmonthly = max (E[Loss] * λ / 12, Pmin)
# Persona A (Alex Chen):
# Pmonthly = max ($226.13 * 1.5 / 12, $20.00) = max($28.27, $20.00) = $28.27
# Persona B (Dr. Brenda Smith):
# Pmonthly = max ($16.20 * 1.5 / 12, $20.00) = max($2.03, $20.00) = $20.00
```