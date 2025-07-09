
import streamlit as st
import plotly.graph_objects as go
import plotly.express as px
import pandas as pd

from application_pages.data_lookups import (
    ROLE_MULTIPLIERS, EDUCATION_LEVEL_FACTORS, EDUCATION_FIELD_FACTORS,
    SCHOOL_TIER_FACTORS, COMPANY_RISK_FACTORS, INDUSTRY_HAZARDS
)
from application_pages.calculations import (
    calculate_human_capital_factor, calculate_company_risk_factor,
    calculate_upskilling_factor, calculate_idiosyncratic_risk,
    calculate_base_occupational_hazard, calculate_systematic_risk,
    calculate_total_payout, calculate_annual_claim_probability,
    calculate_expected_loss, calculate_final_monthly_premium
)

st.set_page_config(page_title="AI-Q Premium Predictor", layout="wide")
st.sidebar.image("https://www.quantuniversity.com/assets/img/logo5.jpg")
st.sidebar.divider()
st.title("AI-Q Premium Predictor")
st.divider()

st.markdown("""
Welcome to the **AI-Q Premium Predictor**, an interactive tool designed to help you understand how a hypothetical AI-driven job displacement insurance premium might be calculated. This application operationalizes a multi-factor parametric framework, illustrating the core concepts from the 'Risk Computation and Premium Determination' section (Section 4) of the AI-Q Score lab.

Our goal is to demystify complex actuarial concepts and demonstrate the "Education is Insurance" paradigm. By adjusting various personal, policy, and environmental parameters, you can visualize how proactive risk mitigation efforts (like upskilling) can directly impact your estimated monthly premium.

### How it Works:

The premium calculation involves several key steps:

1.  **Idiosyncratic Risk ($V_i(t)$):** This assesses your personal vulnerability to job displacement based on your human capital, company stability, and upskilling efforts.
2.  **Systematic Risk ($H_i$):** This reflects the broader occupational hazards and environmental factors like economic climate and AI innovation.
3.  **Annual Claim Probability ($P_{claim}$):** Derived from both Idiosyncratic and Systematic Risks, this is the likelihood of a job displacement event.
4.  **Total Payout Amount ($L_{payout}$):** The financial benefit you would receive if a claim is triggered, based on your salary and coverage.
5.  **Annual Expected Loss ($E[\text{Loss}]$):** The average financial loss expected over a year ($P_{claim} \cdot L_{payout}$).
6.  **Final Monthly Premium ($P_{monthly}$):** Your calculated premium, adjusted for administrative costs and a minimum threshold.

Explore the sidebar to adjust your parameters and see the impact in real-time!
""")

st.markdown("---")

# Sidebar for User Inputs
st.sidebar.header("User Inputs")

st.sidebar.subheader("1. Personal Risk Factors (Idiosyncratic)")

job_role = st.sidebar.selectbox("Job Role", options=list(ROLE_MULTIPLIERS.keys()), index=2) # Mid-level Professional
years_experience = st.sidebar.slider("Years of Experience", min_value=0, max_value=30, value=10)
education_level = st.sidebar.selectbox("Education Level", options=list(EDUCATION_LEVEL_FACTORS.keys()), index=2) # Bachelor's
education_field = st.sidebar.selectbox("Education Field", options=list(EDUCATION_FIELD_FACTORS.keys()), index=3) # Engineering
school_tier = st.sidebar.selectbox("School Tier", options=list(SCHOOL_TIER_FACTORS.keys()), index=1) # Tier 2
company_type = st.sidebar.selectbox("Company Type", options=list(COMPANY_RISK_FACTORS.keys()), index=2) # Big firm
general_upskilling_progress = st.sidebar.slider("General Skills Upskilling Progress (%)", min_value=0, max_value=100, value=50)
firm_specific_upskilling_progress = st.sidebar.slider("Firm-Specific Skills Upskilling Progress (%)", min_value=0, max_value=100, value=20)

st.sidebar.subheader("2. Policy Parameters")
annual_salary = st.sidebar.number_input("Annual Salary ($)", min_value=10000.0, max_value=500000.0, value=90000.0, step=5000.0)
coverage_percentage = st.sidebar.slider("Coverage Percentage (%)", min_value=10, max_value=75, value=25)
coverage_duration_months = st.sidebar.slider("Coverage Duration (Months)", min_value=1, max_value=12, value=6)
beta_systemic = st.sidebar.number_input("Systemic Event Base Probability (β_systemic)", min_value=0.01, max_value=1.0, value=0.10, step=0.01, format="%.2f", help="Calibrated actuarial parameter for systemic displacement.")
beta_individual = st.sidebar.number_input("Individual Loss Base Probability (β_individual)", min_value=0.01, max_value=1.0, value=0.50, step=0.01, format="%.2f", help="Calibrated parameter for job loss for the most vulnerable person.")
lambda_factor = st.sidebar.number_input("Loading Factor (λ)", min_value=1.0, max_value=3.0, value=1.5, step=0.1, format="%.1f", help="Standard insurance multiplier for costs and profit.")
p_min = st.sidebar.number_input("Minimum Premium ($P_{min}$)", min_value=0.0, max_value=100.0, value=20.0, step=5.0, format="%.2f", help="Floor on the monthly premium.")

st.sidebar.subheader("3. Environmental Factors & Career Transition")
economic_climate_modifier = st.sidebar.slider("Economic Climate Modifier ($M_{econ}$)", min_value=0.5, max_value=1.5, value=1.0, step=0.05, help="Reflects economic conditions (e.g., recession < 1.0, boom > 1.0).")
ai_innovation_index = st.sidebar.slider("AI Innovation Index ($I_{AI}$)", min_value=0.5, max_value=1.5, value=1.0, step=0.05, help="Reflects velocity of AI development and adoption.")

current_industry = st.sidebar.selectbox("Current Industry", options=list(INDUSTRY_HAZARDS.keys()), index=4) # Finance/Banking
target_industry = st.sidebar.selectbox("Target Industry (Post-Transition)", options=list(INDUSTRY_HAZARDS.keys()), index=6) # Healthcare
months_elapsed_transition = st.sidebar.slider("Months Elapsed Since Transition ($k$)", min_value=0, max_value=24, value=0, help="Months into a career transition pathway (Time-to-Value, TTV=12 months).")

st.markdown("## Premium Calculation Breakdown")

# --- Calculations ---
# Idiosyncratic Risk (Vi(t))
f_hc = calculate_human_capital_factor(job_role, education_level, education_field, school_tier, years_experience)
f_cr = calculate_company_risk_factor(company_type)
f_us = calculate_upskilling_factor(general_upskilling_progress, firm_specific_upskilling_progress)
v_i = calculate_idiosyncratic_risk(f_hc, f_cr, f_us)

# Systematic Risk (Hi)
h_base_t = calculate_base_occupational_hazard(current_industry, target_industry, months_elapsed_transition)
h_i = calculate_systematic_risk(h_base_t, economic_climate_modifier, ai_innovation_index)

# Premium Determination
l_payout = calculate_total_payout(annual_salary, coverage_percentage, coverage_duration_months)
p_claim = calculate_annual_claim_probability(h_i, v_i, beta_systemic, beta_individual)
e_loss = calculate_expected_loss(p_claim, l_payout)
p_monthly = calculate_final_monthly_premium(e_loss, lambda_factor, p_min)

# --- Display Results ---

# Idiosyncratic Risk Expander
with st.expander("### 1. Idiosyncratic Risk ($V_i(t)$) Details"):
    st.markdown("""
    Your personal vulnerability to job displacement, assessed by your human capital, company stability, and upskilling efforts.
    The raw score is a weighted product: $V_{raw} = F_{HC} \cdot (w_{CR} \cdot F_{CR} + w_{US} \cdot F_{US})$
    And the final score is normalized: $V_i(t) = \min(100.0, \max(5.0, V_{raw} - 50.0))$
    """)
    
    st.subheader("Human Capital Factor ($F_{HC}$)")
    st.markdown(r"$$F_{HC} = f_{role} \cdot f_{level} \cdot f_{field} \cdot f_{school} \cdot f_{exp}$$")
    st.info(f"**Calculated F_HC:** `{f_hc:.2f}`")
    
    st.subheader("Company Risk Factor ($F_{CR}$)")
    st.info(f"**Calculated F_CR:** `{f_cr:.2f}` (Based on company type)")

    st.subheader("Upskilling Factor ($F_{US}$)")
    st.markdown(r"$$F_{US} = 1 - (\gamma_{gen} \cdot P_{gen}(t) + \gamma_{spec} \cdot P_{spec}(t))$$")
    st.info(f"**Calculated F_US:** `{f_us:.2f}`")

    st.subheader("Final Idiosyncratic Risk ($V_i(t)$)")
    st.markdown(f"**V_raw calculation:** `F_HC * (W_CR * F_CR + W_US * F_US)` (using default weights 0.4 and 0.6)")
    st.metric(label="Your Idiosyncratic Risk Score", value=f"{v_i:.2f}")
# Systematic Risk Expander
with st.expander("### 2. Systematic Risk ($H_i$) Details"):
    st.markdown("""
    This score accounts for macro-level risks inherent to an occupation, influenced by economic conditions and AI advancements.
    $$H_i = H_{base}(t) \cdot (w_{econ} \cdot M_{econ} + w_{inno} \cdot I_{AI})$$
    """)

    st.subheader("Base Occupational Hazard ($H_{base}(t)$)")
    st.markdown(r"$$H_{base}(k) = \left(1 - \frac{k}{TTV}\right) \cdot H_{current} + \left(\frac{k}{TTV}\right) \cdot H_{target}$$")
    st.info(f"**Calculated H_base(t):** `{h_base_t:.2f}` (Adjusted for career transition over {months_elapsed_transition} months)")

    st.subheader("Environmental Modifiers ($M_{econ}$, $I_{AI}$)")
    st.info(f"**Economic Climate Modifier (M_econ):** `{economic_climate_modifier:.2f}`")
    st.info(f"**AI Innovation Index (I_AI):** `{ai_innovation_index:.2f}`")

    st.subheader("Final Systematic Risk ($H_i$)")
    st.metric(label="Your Systematic Risk Score", value=f"{h_i:.2f}")


# Claim & Loss Calculation Expander
with st.expander("### 3. Claim & Loss Calculation"):
    st.subheader("Total Payout Amount ($L_{payout}$)")
    st.markdown(r"$$L_{payout} = \frac{Annual\ Salary}{12} \cdot Coverage\ Duration \cdot Coverage\ Percentage$$")
    st.info(f"**Calculated L_payout:** `${l_payout:,.2f}`")

    st.subheader("Annual Claim Probability ($P_{claim}$)")
    st.markdown(r"$$P_{claim} = \left(\frac{H_i}{100} \cdot \eta_{systemic}\right) \cdot \left(\frac{V_i(t)}{100} \cdot \eta_{individual}\right)$$")
    st.info(f"**Calculated P_claim:** `{p_claim:.4f}`")

    st.subheader("Annual Expected Loss ($E[\text{Loss}]$)")
    st.markdown(r"$$E[\text{Loss}] = P_{claim} \cdot L_{payout}$$")
    st.info(f"**Calculated E[Loss]:** `${e_loss:,.2f}`")

st.markdown("## Final Monthly Premium\n ")
st.markdown(r"""
This is the final cost to you for the hypothetical AI-driven job displacement insurance. It ensures coverage for administrative costs and profit margins (through the Loading Factor) and meets a minimum policy viability threshold.
""")
st.markdown(r"$$ P_{monthly} = \max\left(\frac{E[\text{Loss}] \cdot \lambda}{12}, P_{min}\right) $$")

col1, col2 = st.columns([1, 2])

with col1:
    # Gauge chart for monthly premium
    fig = go.Figure(go.Indicator(
        mode = "gauge+number",
        value = p_monthly,
        title = {'text': "Calculated Monthly Premium"},
        gauge = {'axis': {'range': [p_min, 100 + p_min], 'tickwidth': 1, 'tickcolor': "darkblue"},
                 'bar': {'color': "darkblue"},
                 'steps': [
                     {'range': [p_min, p_min + 20], 'color': "lightgreen"},
                     {'range': [p_min + 20, p_min + 50], 'color': "lightyellow"},
                     {'range': [p_min + 50, p_min + 100], 'color': "lightcoral"}],
                 'threshold' : {'line': {'color': "red", 'width': 4}, 'thickness': 0.75, 'value': p_min + 75}}
    ))
    fig.update_layout(margin=dict(l=20, r=20, t=50, b=20))
    st.plotly_chart(fig, use_container_width=True)

with col2:
    st.metric(label="Your Estimated Monthly Premium", value=f"${p_monthly:.2f}")
    if p_monthly <= p_min:
        st.info(f"Note: Your calculated premium hit the minimum threshold of ${p_min:.2f}.")
    
    st.subheader("Contribution Breakdown")
    data = {
        'Factor': ['Human Capital (F_HC)', 'Company Risk (F_CR)', 'Upskilling (F_US)'],
        'Value': [f_hc, f_cr, f_us]
    }
    df_idiosyncratic = pd.DataFrame(data)
    fig_idiosyncratic = px.bar(df_idiosyncratic, x='Factor', y='Value', 
                               title='Idiosyncratic Risk Factor Contributions',
                               color='Factor',
                               color_discrete_map={
                                   'Human Capital (F_HC)': 'lightblue',
                                   'Company Risk (F_CR)': 'lightcoral',
                                   'Upskilling (F_US)': 'lightgreen'
                               })
    st.plotly_chart(fig_idiosyncratic, use_container_width=True)

    data_sys = {
        'Factor': ['Base Occupational Hazard', 'Economic Climate', 'AI Innovation'],
        'Value': [h_base_t, economic_climate_modifier * 100, ai_innovation_index * 100] # Scale for better visualization
    }
    df_systematic = pd.DataFrame(data_sys)
    fig_systematic = px.bar(df_systematic, x='Factor', y='Value', 
                            title='Systematic Risk Component Contributions (Scaled)',
                            color='Factor',
                            color_discrete_map={
                                'Base Occupational Hazard': 'lightgray',
                                'Economic Climate': 'lightgoldenrodyellow',
                                'AI Innovation': 'lightpink'
                            })
    st.plotly_chart(fig_systematic, use_container_width=True)


st.markdown("## Education is Insurance")
st.markdown("""
This application highlights the principle that **"Education is Insurance"**. By interacting with the sliders and dropdowns, you can observe how certain choices and efforts directly translate into your calculated premium:

*   **Upskilling:** Increasing your "General Skills Upskilling Progress" (portable skills) will generally **lower** your Idiosyncratic Risk, and thus your premium. This reflects the increased adaptability and marketability you gain.
*   **Career Transition:** A strategic "Target Industry" choice, especially one with a lower `H_base` score, can reduce your Systematic Risk over time. The "Months Elapsed Since Transition" slider demonstrates how this benefit accrues gradually.
*   **Education & Experience:** Higher education levels, specialized fields (like Engineering/Quant), and relevant experience can also contribute to a **lower** Human Capital Factor, reducing your overall Idiosyncratic Risk.

This demonstrates how investing in your human capital and making informed career decisions can act as a form of self-insurance against the risks of AI-driven job displacement.
""")

st.divider()
st.write("© 2025 QuantUniversity. All Rights Reserved.")
st.caption("The purpose of this demonstration is solely for educational use and illustration. "
           "Any reproduction of this demonstration "
           "requires prior written consent from QuantUniversity. "
           "This lab was generated using the QuCreate platform. QuCreate relies on AI models for generating code, which may contain inaccuracies or errors.")
