import streamlit as st
import pandas as pd
import numpy as np
from src.model_pipeline import load_and_preprocess_data, train_and_evaluate_models

st.set_page_config(page_title="Predictive Churn Risk Engine", layout="wide")

st.title("🔮 Predictive Modeling & Risk Scoring for Bank Customer Churn")
st.markdown("---")

# Load and Train Models
@st.cache_resource
def run_ml_pipeline():
    X_train, X_test, y_train, y_test = load_and_preprocess_data()
    preprocessor, results = train_and_evaluate_models(X_train, X_test, y_train, y_test)
    return preprocessor, results, X_test, y_test

preprocessor, results, X_test, y_test = run_ml_pipeline()

# Sidebar: Selection
st.sidebar.header("⚙️ Machine Learning Controls")
selected_model_name = st.sidebar.selectbox("Select Classification Algorithm", list(results.keys()))

selected_model = results[selected_model_name]['model_object']

# Tab Layout
tab1, tab2 = st.tabs(["📊 Model Evaluation", "🧮 Individual Risk Calculator"])

with tab1:
    st.subheader("Model Performance Benchmark")
    eval_df = pd.DataFrame(results).T.drop(columns=['model_object'])
    st.dataframe(eval_df.style.highlight_max(axis=0, color='#d4edda'))
    
    st.markdown("""
    * **Recall:** Critical metric ensuring the bank captures actual potential churners before they exit.
    * **ROC-AUC:** Demonstrates high classification confidence across varying probability thresholds.
    """)

with tab2:
    st.subheader("Customer Risk Scoring Calculator")
    
    col1, col2, col3 = st.columns(3)
    with col1:
        credit_score = st.number_input("Credit Score", 300, 850, 650)
        age = st.number_input("Age", 18, 100, 42)
        tenure = st.number_input("Tenure (Years)", 0, 10, 5)
    with col2:
        balance = st.number_input("Balance (€)", 0.0, 250000.0, 75000.0)
        num_products = st.selectbox("Number of Products", [1, 2, 3, 4], index=0)
        estimated_salary = st.number_input("Estimated Salary (€)", 0.0, 200000.0, 100000.0)
    with col3:
        geography = st.selectbox("Geography", ["France", "Germany", "Spain"])
        gender = st.selectbox("Gender", ["Male", "Female"])
        has_cr_card = st.selectbox("Has Credit Card?", [1, 0])
        is_active = st.selectbox("Is Active Member?", [1, 0])
        
    # Feature Engineering Calculations
    bal_to_sal = balance / (estimated_salary + 1)
    prod_density = num_products / (tenure + 1)
    age_tenure = age / (tenure + 1)
    active_multi = 1 if (is_active == 1 and num_products > 1) else 0
    
    input_df = pd.DataFrame([{
        'CreditScore': credit_score, 'Geography': geography, 'Gender': gender,
        'Age': age, 'Tenure': tenure, 'Balance': balance, 'NumOfProducts': num_products,
        'HasCrCard': has_cr_card, 'IsActiveMember': is_active, 'EstimatedSalary': estimated_salary,
        'BalanceToSalary': bal_to_sal, 'ProductDensity': prod_density,
        'AgeTenureRatio': age_tenure, 'IsActiveAndMultiProduct': active_multi
    }])
    
    input_prep = preprocessor.transform(input_df)
    churn_prob = selected_model.predict_proba(input_prep)[0][1]
    
    st.markdown("### Risk Prediction Output")
    st.metric("Calculated Churn Probability Score", f"{churn_prob * 100:.2f}%")
    
    if churn_prob > 0.5:
        st.error("🚨 **HIGH CHURN RISK:** Immediate proactive retention campaign required.")
    elif churn_prob > 0.25:
        st.warning("⚠️ **MODERATE RISK:** Monitor digital activity and cross-sell engagement.")
    else:
        st.success("✅ **LOW RISK:** Customer relationship is stable.")
