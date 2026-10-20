import streamlit as st
import pandas as pd
import numpy as np

# Page Configuration
st.set_page_config(
    page_title="European Bank Churn Risk Dashboard",
    page_icon="🏦",
    layout="wide"
)

# Load Data Safely from the 'data/' folder with a Fallback
@st.cache_data
def load_data():
    file_path = "data/European_Bank (1).csv"
    try:
        return pd.read_csv(file_path), True
    except FileNotFoundError:
        # Fallback sample data so the app never throws a hard crash
        np.random.seed(42)
        n = 1000
        df_sample = pd.DataFrame({
            'CreditScore': np.random.randint(350, 850, n),
            'Geography': np.random.choice(['France', 'Spain', 'Germany'], n),
            'Age': np.random.randint(18, 70, n),
            'Balance': np.random.uniform(0, 150000, n),
            'Exited': np.random.choice([0, 1], n, p=[0.8, 0.2]),
            'Tenure': np.random.randint(0, 10, n),
            'EstimatedSalary': np.random.uniform(20000, 150000, n)
        })
        return df_sample, False

df, file_exists = load_data()

# Show a warning ONLY if it falls back to sample data (hides the success banner)
if not file_exists:
    st.warning("⚠️ 'data/European_Bank (1).csv' was not found. Currently displaying sample dashboard data. Check your GitHub repository structure.")

# --- SIDEBAR: Advanced Filters ---
st.sidebar.header("🔍 Advanced Filters")
st.sidebar.markdown("Slice and dice customer segments dynamically.")

# 1. Geography Filter
countries = ["All"] + list(df['Geography'].unique()) if 'Geography' in df.columns else ["All"]
selected_country = st.sidebar.selectbox("Country", options=countries)

# 2. Gender Filter (NEW)
genders = ["All"] + list(df['Gender'].unique()) if 'Gender' in df.columns else ["All"]
selected_gender = st.sidebar.selectbox("Gender", options=genders)

# 3. Age Range Slider
min_age = int(df['Age'].min()) if 'Age' in df.columns else 18
max_age = int(df['Age'].max()) if 'Age' in df.columns else 100
age_range = st.sidebar.slider("Age Range", min_age, max_age, (min_age, max_age))

# 4. Credit Score Slider (NEW)
min_cs = int(df['CreditScore'].min()) if 'CreditScore' in df.columns else 300
max_cs = int(df['CreditScore'].max()) if 'CreditScore' in df.columns else 850
credit_range = st.sidebar.slider("Credit Score Range", min_cs, max_cs, (min_cs, max_cs))

# 5. Activity Status Filter (NEW)
activity_options = ["All", "Active Member", "Inactive Member"]
selected_activity = st.sidebar.selectbox("Activity Status", options=activity_options)

# --- Apply All Filters Safely ---
filtered_df = df.copy()

if selected_country != "All" and 'Geography' in df.columns:
    filtered_df = filtered_df[filtered_df['Geography'] == selected_country]

if selected_gender != "All" and 'Gender' in df.columns:
    filtered_df = filtered_df[filtered_df['Gender'] == selected_gender]

if 'Age' in df.columns:
    filtered_df = filtered_df[(filtered_df['Age'] >= age_range[0]) & (filtered_df['Age'] <= age_range[1])]

if 'CreditScore' in df.columns:
    filtered_df = filtered_df[(filtered_df['CreditScore'] >= credit_range[0]) & (filtered_df['CreditScore'] <= credit_range[1])]

if selected_activity == "Active Member" and 'IsActiveMember' in df.columns:
    filtered_df = filtered_df[filtered_df['IsActiveMember'] == 1]
elif selected_activity == "Inactive Member" and 'IsActiveMember' in df.columns:
    filtered_df = filtered_df[filtered_df['IsActiveMember'] == 0]

st.sidebar.markdown("---")
st.sidebar.markdown(f"**Filtered Customers:** `{len(filtered_df):,}` / `{len(df):,}`")

# --- MAIN TITLE ---
st.title("🏦 European Bank Churn Risk Dashboard")
st.markdown("Explore customer trends and test individual risk scenarios below.")
st.markdown("---")

# --- TOP METRICS ---
col1, col2, col3, col4 = st.columns(4)
col1.metric("Total Customers", f"{len(filtered_df):,}")
col2.metric("Avg Credit Score", int(filtered_df['CreditScore'].mean()) if 'CreditScore' in filtered_df.columns else 0)
col3.metric("Overall Churn Rate", f"{(filtered_df['Exited'].mean() * 100):.1f}%" if 'Exited' in filtered_df.columns else "0%")
col4.metric("Avg Balance", f"${filtered_df['Balance'].mean():,.2f}" if 'Balance' in filtered_df.columns else "$0.00")

st.markdown("---")

# --- TABS ---
tab1, tab2, tab3 = st.tabs(["📊 Overview", "🔮 Customer Simulator", "📁 Raw Data & Export"])

with tab1:
    st.subheader("Data Insights")
    c1, c2 = st.columns(2)
    with c1:
        st.markdown("**Churn Rate by Age**")
        if 'Age' in filtered_df.columns and 'Exited' in filtered_df.columns:
            st.line_chart(filtered_df.groupby('Age')['Exited'].mean())
        else:
            st.info("Chart data unavailable.")
    with c2:
        st.markdown("**Balance Distribution (Sample)**")
        if 'Balance' in filtered_df.columns:
            st.bar_chart(filtered_df['Balance'].head(40))
        else:
            st.info("Chart data unavailable.")

with tab2:
    st.subheader("🔮 Individual Customer Churn Risk Simulator")
    st.markdown("Adjust customer attributes using the controls below to calculate their real-time churn probability.")

    with st.form("prediction_form"):
        col1, col2 = st.columns(2)
        
        with col1:
            credit_score = st.slider("Credit Score", 300, 850, 650, help="Customer's credit score")
            age = st.slider("Age", 18, 92, 40, help="Customer's age in years")
            tenure = st.slider("Tenure (Years)", 0, 10, 5, help="Number of years the customer has been with the bank")
            balance = st.number_input("Account Balance ($)", 0.0, 250000.0, 50000.0)
            geography = st.selectbox("Geography (Country)", ["France", "Germany", "Spain"])
            
        with col2:
            gender = st.selectbox("Gender", ["Female", "Male"])
            num_of_products = st.selectbox("Number of Bank Products", [1, 2, 3, 4])
            has_cr_card = st.selectbox("Has Credit Card?", [1, 0], format_func=lambda x: "Yes" if x == 1 else "No")
            is_active_member = st.selectbox("Is Active Member?", [1, 0], format_func=lambda x: "Yes" if x == 1 else "No")
            estimated_salary = st.number_input("Estimated Salary ($)", 0.0, 200000.0, 50000.0)

        submit_btn = st.form_submit_button("Calculate Churn Risk", type="primary")

    if submit_btn:
        # Create a DataFrame for the single customer input
        input_dict = {
            'CreditScore': [credit_score],
            'Age': [age],
            'Tenure': [tenure],
            'Balance': [balance],
            'NumOfProducts': [num_of_products],
            'HasCrCard': [has_cr_card],
            'IsActiveMember': [is_active_member],
            'EstimatedSalary': [estimated_salary],
            'Geography': [geography],
            'Gender': [gender]
        }
        input_df = pd.DataFrame(input_dict)
        
        # --- MODEL PREDICTION LOGIC ---
        # If you have a trained model saved (e.g., joblib/pickle), load and predict here:
        # model = joblib.load('model.pkl')
        # churn_prob = model.predict_proba(input_df)[0][1]
        
        # Dynamic Risk Simulation based on standard bank churn behavior (Fallback / baseline)
        risk_score = 0.10 # Base risk
        if age > 45: risk_score += 0.20
        if is_active_member == 0: risk_score += 0.15
        if geography == "Germany": risk_score += 0.15
        if num_of_products > 2: risk_score += 0.25
        if balance > 100000: risk_score += 0.05
        
        churn_prob = min(max(risk_score, 0.02), 0.95) # Keep between 2% and 95%
        
        st.markdown("---")
        st.subheader("Simulation Results")
        
        res_col1, res_col2 = st.columns(2)
        with res_col1:
            st.metric(
                label="Estimated Churn Probability", 
                value=f"{churn_prob * 100:.1f}%",
                delta="High Risk" if churn_prob > 0.4 else "Low Risk",
                delta_color="inverse"
            )
        with res_col2:
            if churn_prob > 0.4:
                st.error("⚠️ **High Risk Alert:** This customer exhibits strong indicators of churning. Consider offering a retention incentive or loyalty discount.")
            else:
                st.success("✅ **Low Risk:** This customer is stable and likely to stay with the bank.")
                
        # Optional: Display the processed profile back to the user
        with st.expander("View Customer Profile Submitted"):
            st.dataframe(input_df, use_container_width=True)

with tab3:
    st.subheader("Filtered Dataset View")
    st.dataframe(filtered_df.head(100), use_container_width=True)
    st.download_button(
        "Download Filtered Data as CSV",
        filtered_df.to_csv(index=False).encode('utf-8'),
        "filtered_bank_data.csv",
        "text/csv"
    )
