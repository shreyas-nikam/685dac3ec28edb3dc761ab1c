
# AI-Q Premium Predictor: A Multi-Factor Parametric Framework for Quantifying and Mitigating AI-Driven Job Displacement Risk

## Overview

The AI-Q Premium Predictor is an interactive Streamlit application designed to help users understand and estimate a hypothetical AI-driven job displacement insurance premium. It operationalizes the actuarial model outlined in the accompanying document, specifically focusing on the 'Risk Computation and Premium Determination' section (Section 4). This application aims to demystify complex financial concepts and illustrate the "Education is Insurance" paradigm by demonstrating how proactive risk mitigation efforts can lead to lower premiums.

## Core Concepts and Mathematical Foundations

The application is built upon several interconnected mathematical concepts. Users can adjust various parameters to see their impact on the calculated premium.

### Idiosyncratic Risk ($V_i(t)$)

Idiosyncratic Risk, or Vulnerability, assesses an individual's specific vulnerability to job displacement. It is calculated as a composite of the Human Capital Factor ($F_{HC}$), Company Risk Factor ($F_{CR}$), and Upskilling Factor ($F_{US}$), then normalized.

The general form is:
$$
V_i(t) = f(F_{HC}, F_{CR}, F_{US})
$$
The raw score ($V_{raw}$) is a weighted product:
$$
V_{raw} = F_{HC} \cdot (w_{CR} \cdot F_{CR} + w_{US} \cdot F_{US})
$$
The final $V_i(t)$ is normalized:
$$
V_i(t) = \min(100.0, \max(5.0, V_{raw} - 50.0))
$$

- **Human Capital Factor ($F_{HC}$):** Assesses foundational resilience based on educational and professional background.
  $$
  F_{HC} = f_{role} \cdot f_{level} \cdot f_{field} \cdot f_{school} \cdot f_{exp}
  $$
- **Company Risk Factor ($F_{CR}$):** Quantifies the stability and growth prospects of the individual's current employer.
  $$
  F_{CR} = w_1 \cdot S_{senti} + w_2 \cdot S_{fin} + w_3 \cdot S_{growth}
  $$
- **Upskilling Factor ($F_{US}$):** Differentiates between skill types, rewarding portable skills more heavily.
  $$
  F_{US} = 1 - (\gamma_{gen} \cdot P_{gen}(t) + \gamma_{spec} \cdot P_{spec}(t))
  $$

### Systematic Risk ($H_i$)

Systematic Risk is a dynamic index reflecting occupational hazard and the broader environment.
$$
H_i = H_{base}(t) \cdot (w_{econ} \cdot M_{econ} + w_{inno} \cdot I_{AI})
$$
- **Base Occupational Hazard ($H_{base}(t)$):** Changes over time based on career transition.
  $$
  H_{base}(k) = \left(1 - \frac{k}{TTV}\right) \cdot H_{current} + \left(\frac{k}{TTV}\right) \cdot H_{target}
  $$
- **Environmental Modifiers ($M_{econ}$, $I_{AI}$):** Dynamically adjust risk based on economic climate and AI innovation.

### Total Payout Amount ($L_{payout}$)

The total amount paid if a claim is triggered, defined by policy terms.
$$
L_{payout} = \frac{Annual\ Salary}{12} \cdot Coverage\ Duration \cdot Coverage\ Percentage
$$

### Annual Claim Probability ($P_{claim}$)

The annual probability of a claim, modeled as the joint probability of a systemic event and individual loss.
$$
P_{claim} = \left(\frac{H_i}{100} \cdot \beta_{systemic}\right) \cdot \left(\frac{V_i(t)}{100} \cdot \beta_{individual}\right)
$$

### Annual Expected Loss ($E[\text{Loss}]$)

The expected loss is the total payout amount multiplied by the probability of a claim.
$$
E[\text{Loss}] = P_{claim} \cdot L_{payout}
$$

### Final Monthly Premium ($P_{monthly}$)

The final monthly premium, adjusted by a loading factor and a minimum premium threshold.
$$
P_{monthly} = \max\left(\frac{E[\text{Loss}] \cdot \lambda}{12}, P_{min}\right)
$$

## Setup and Running the Application

To run the AI-Q Premium Predictor application locally, follow these steps:

1.  **Clone the Repository:**
    ```bash
    git clone <repository-url>
    cd ai-q-premium-predictor
    ```

2.  **Create a Virtual Environment (Recommended):**
    ```bash
    python -m venv venv
    # On Windows:
    # .\venv\Scripts\activate
    # On macOS/Linux:
    # source venv/bin/activate
    ```

3.  **Install Dependencies:**
    ```bash
    pip install -r requirements.txt
    ```

4.  **Run the Streamlit Application:**
    ```bash
    streamlit run app.py
    ```

    This will open the application in your default web browser.

## Docker Deployment (Optional)

You can also run the application using Docker:

1.  **Build the Docker Image:**
    ```bash
    docker build -t ai-q-predictor .
    ```

2.  **Run the Docker Container:**
    ```bash
    docker run -p 8501:8501 ai-q-predictor
    ```

    Then, open your web browser and navigate to `http://localhost:8501`.

---

© 2025 QuantUniversity. All Rights Reserved.
The purpose of this demonstration is solely for educational use and illustration. Any reproduction of this demonstration requires prior written consent from QuantUniversity. This lab was generated using the QuCreate platform. QuCreate relies on AI models for generating code, which may contain inaccuracies or errors.
