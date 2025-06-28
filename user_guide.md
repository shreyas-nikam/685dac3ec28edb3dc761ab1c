id: 685dac3ec28edb3dc761ab1c_user_guide
summary: AI-Q Score: A Multi-Factor Parametric Framework for Quantifying and Mitigating AI-Driven Job Displacement Risk User Guide
feedback link: https://docs.google.com/forms/d/e/1FAIpQLSfWkOK-in_bMMoHSZfcIvAeO58PAH9wrDqcxnJABHaxiDqhSA/viewform?usp=sf_link
environments: Web
status: Published
# AI-Q Premium Predictor: A Codelab User Guide

This codelab guides you through the AI-Q Premium Predictor, a Streamlit application designed to illustrate how an AI-driven job displacement insurance premium could be calculated. The application showcases core concepts from the AI-Q Score lab, particularly the "Risk Computation and Premium Determination" framework. It highlights the importance of proactive risk mitigation, such as upskilling, and its impact on insurance premiums, reinforcing the idea that "Education is Insurance".

## Understanding the Application's Functionality
Duration: 00:05

This application uses a multi-factor parametric framework to calculate a hypothetical insurance premium. It breaks down the calculation into understandable steps, allowing you to explore the impact of various factors on the final premium. The application doesn't predict real-world premiums, but rather it is for educational purposes and illustrating underlying concepts.

<aside class="positive">
<b>Key Concept:</b> The application helps understand how personal and environmental factors can influence the risk of job displacement and, consequently, the insurance premium.
</aside>

## Navigating the User Interface
Duration: 00:03

The application is structured into two main sections: the sidebar and the main panel.

*   **Sidebar:** Contains interactive input widgets for adjusting various parameters related to personal risk factors, policy parameters, and environmental factors.
*   **Main Panel:** Displays a breakdown of the premium calculation, including intermediate factors and the final monthly premium, along with visualizations to illustrate the contribution of different factors.

## Inputting Personal Risk Factors (Idiosyncratic)
Duration: 00:07

The "Personal Risk Factors (Idiosyncratic)" section in the sidebar allows you to define your individual circumstances. These factors contribute to your Idiosyncratic Risk, reflecting your personal vulnerability to job displacement.

1.  **Job Role:** Select your current job role from the dropdown menu. Different roles have varying multipliers affecting the Human Capital Factor.
2.  **Years of Experience:** Use the slider to specify your years of relevant work experience. More experience generally reduces your risk.
3.  **Education Level:** Choose your highest level of education. Higher education typically reduces your risk.
4.  **Education Field:** Select the field of your education. Certain fields are considered more resilient to job displacement.
5.  **School Tier:** Indicate the tier of the institution where you received your education. Higher-tier schools often imply a reduced risk.
6.  **Company Type:** Choose the type of company you work for. Different company types carry different levels of risk (e.g., startups are generally riskier than large firms).
7.  **General Skills Upskilling Progress (%):** Use the slider to indicate your progress in acquiring general, portable skills.
8.  **Firm-Specific Skills Upskilling Progress (%):** Indicate your progress in acquiring skills specific to your current firm.

<aside class="positive">
<b>Tip:</b> Experiment with different combinations of these factors to observe how they affect your Idiosyncratic Risk and, ultimately, your premium.
</aside>

## Adjusting Policy Parameters
Duration: 00:05

The "Policy Parameters" section in the sidebar defines the terms of the hypothetical insurance policy.

1.  **Annual Salary ($):** Enter your current annual salary. This value is used to calculate the total payout amount in case of a claim.
2.  **Coverage Percentage (%):** Specify the percentage of your salary that the policy will cover.
3.  **Coverage Duration (Months):** Define the duration, in months, for which the policy will provide coverage.
4.  **Systemic Event Base Probability (β_systemic):** This parameter reflects the base probability of a systemic event causing job displacement.
5.  **Individual Loss Base Probability (β_individual):** This parameter reflects the base probability of job loss for a vulnerable individual.
6.  **Loading Factor (λ):** This is a standard insurance multiplier that accounts for administrative costs and profit margins.
7.  **Minimum Premium ($P_{min}$):** This represents the floor on the monthly premium, ensuring policy viability.

<aside class="negative">
<b>Note:</b> The systemic and individual loss base probabilities are calibrated actuarial parameters that significantly influence the claim probability.
</aside>

## Setting Environmental Factors & Career Transition
Duration: 00:05

The "Environmental Factors & Career Transition" section in the sidebar allows you to specify broader economic and industry-specific conditions.

1.  **Economic Climate Modifier ($M_{econ}$):** Use the slider to reflect the prevailing economic conditions. Values below 1.0 represent a recession, while values above 1.0 indicate a boom.
2.  **AI Innovation Index ($I_{AI}$):** Adjust the slider to reflect the pace of AI development and adoption.
3.  **Current Industry:** Select your current industry from the dropdown menu.
4.  **Target Industry (Post-Transition):** Choose your target industry, the industry you are transitioning to.
5.  **Months Elapsed Since Transition ($k$):** Indicate the number of months you have been in the process of transitioning to the target industry.

<aside class="positive">
<b>Concept:</b> These environmental factors influence the Systematic Risk, reflecting the broader risks inherent to your occupation.
</aside>

## Interpreting the Premium Calculation Breakdown
Duration: 00:10

The main panel displays a step-by-step breakdown of the premium calculation, allowing you to understand how the various factors contribute to the final result.

1.  **Idiosyncratic Risk ($V_i(t)$) Details:** This section provides a detailed explanation of how your personal risk factors are combined to calculate your Idiosyncratic Risk score. It includes formulas for the Human Capital Factor ($F_{HC}$), Company Risk Factor ($F_{CR}$), and Upskilling Factor ($F_{US}$).
2.  **Systematic Risk ($H_i$) Details:** This section explains how environmental factors influence the Systematic Risk score. It includes the formula for Base Occupational Hazard ($H_{base}(t)$) and shows how economic climate and AI innovation are factored in.
3.  **Claim & Loss Calculation:** This section details the calculation of the Total Payout Amount ($L_{payout}$), Annual Claim Probability ($P_{claim}$), and Annual Expected Loss ($E[\text{Loss}]$).

<aside class="positive">
<b>Key Insight:</b> By examining these sections, you can see how each factor influences the final premium.
</aside>

## Analyzing the Final Monthly Premium and Factor Contributions
Duration: 00:05

The "Final Monthly Premium" section displays the calculated monthly premium and provides a visual breakdown of the contributions from different factors.

*   **Gauge Chart:** A gauge chart visually represents the calculated monthly premium, indicating its position within a defined range.
*   **Estimated Monthly Premium:** The final calculated monthly premium is displayed as a metric.
*   **Contribution Breakdown:** Bar charts illustrate the relative contributions of different factors to the Idiosyncratic Risk and Systematic Risk scores.

<aside class="positive">
<b>Insight:</b> The contribution breakdown allows you to identify the factors that have the most significant impact on your premium.
</aside>

## Understanding "Education is Insurance"
Duration: 00:05

The application highlights the principle that "Education is Insurance." By interacting with the application, you can observe how certain choices and efforts directly translate into your calculated premium.

*   **Upskilling:** Increasing your "General Skills Upskilling Progress" (portable skills) will generally **lower** your Idiosyncratic Risk, and thus your premium.
*   **Career Transition:** A strategic "Target Industry" choice, especially one with a lower `H_base` score, can reduce your Systematic Risk over time.
*   **Education & Experience:** Higher education levels, specialized fields, and relevant experience can also contribute to a **lower** Human Capital Factor, reducing your overall Idiosyncratic Risk.

<aside class="positive">
<b>Takeaway:</b> Investing in your human capital and making informed career decisions can act as a form of self-insurance against the risks of AI-driven job displacement.
</aside>
