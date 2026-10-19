import streamlit as st
import pandas as pd
import os

# 1. Page Configuration (Must be the first Streamlit command)
st.set_page_config(
    page_title="European Bank Churn Risk Dashboard",
    page_icon="🏦",
    layout="wide",
    initial_sidebar_state="expanded"
)

# 2. Load Data Safely
# Assuming your data loading function is in src/model_pipeline.py
try:
    from src.model_pipeline import load_and_preprocess_data
    df = load_and_preprocess_data()
except Exception as e:
    # Fallback direct read if pipeline import fails or isn't set up yet
    current_dir = os.path.dirname(os.path.abspath(__file__))
    csv_path = os.path.join(current_dir, "European_Bank (1).csv")
    df = pd.read_csv(csv_path)

# --- SIDEBAR: Filters & Controls ---
st.sidebar.header("🔍 Dashboard Filters")
st.sidebar.markdown("Slice and dice the dataset safely without altering source data.")

# Geography Filter (Check if column exists)
if 'Geography' in df.columns:
    countries = ["All"] + list(df['Geography'].unique())
    selected_country = st.sidebar.selectbox("Select Country", options=countries)
else:
    selected_country = "All"

# Age Range Filter
if 'Age' in df.columns:
    min_age, max_age = int(df['Age'].min()), int(df['Age'].max())
    age_range = st.sidebar.slider("Select Age Range", min_age, max_age, (min_age, max_age))
else:
    age_range = (18, 100)

# Apply filters safely to a copy of the dataframe
filtered_df = df.copy()
if selected_country != "All" and 'Geography' in df.columns:
    filtered_df = filtered_df[filtered_df['Geography'] == selected_country]
if 'Age' in df.columns:
    filtered_df = filtered_df[(filtered_df['Age'] >= age_range[0]) & (filtered_df['Age'] <= age_range[1])]

st.sidebar.markdown("---")
st.sidebar.markdown(f"**Active Customers in View:** `{len(filtered_df):,}`")


# --- MAIN PAGE HEADER ---
st.title("🏦 European Bank Churn Risk Analytics")
st.markdown("Welcome to your interactive risk intelligence dashboard. Use the tabs below to explore data insights or test customer risk scenarios.")
st.markdown("---")


# --- TOP KPI METRICS ---
col1, col2, col3, col4 = st.columns(4)
total_cust = len(filtered_df)
avg_credit = int(filtered_df['CreditScore'].mean()) if 'CreditScore' in filtered_df.columns else 0
churn_rate = (filtered_df['Exited'].mean() * 100) if 'Exited' in filtered_df.columns else 0.0
avg_balance = filtered_df['Balance'].mean() if 'Balance' in filtered_df.columns else 0.0

col1.metric(label="Total Customers", value=f"{total_cust:,}")
col2.metric(label="Avg Credit Score", value=avg_credit)
col3.metric(label="Overall Churn Rate", value=f"{churn_rate:.1f}%")
col4.metric(label="Avg Account Balance", value=f"${avg_balance:,.2f}")

st.markdown("---")


# --- NAVIGATION TABS ---
tab1, tab2, tab3 = st.tabs(["📊 Overview & Insights", "🔮 Single Customer Predictor", "📁 Raw Data & Export"])

# TAB 1: OVERVIEW & INSIGHTS
with tab1:
    st.subheader("Visualizing Customer Trends")
    
    col_chart1, col_chart2 = st.columns(2)
    
    with col_chart1:
        st.markdown("**Churn Rate by Age**")
        if 'Age' in filtered_df.columns and 'Exited' in filtered_df.columns:
            age_churn = filtered_df.groupby('Age')['Exited'].mean()
            st.line_chart(age_churn)
        else:
            st.info("Required columns for age chart not found.")
            
    with col_chart2:
        st.markdown("**Account Balance Distribution (Sample)**")
        if 'Balance' in filtered_df.columns:
            st.bar_chart(filtered_df['Balance'].head(40))
        else:
            st.info("Balance column not found.")


# TAB 2: SINGLE CUSTOMER PREDICTOR ("WHAT-IF" SIMULATOR)
with tab2:
    st.subheader("🔮 Individual Customer Churn Risk Simulator")
    st.markdown("Adjust customer attributes using the controls below and click calculate to estimate churn probability.")

    with st.form("prediction_form"):
        p_col1, p_col2 = st.columns(2)
        
        with p_col1:
            credit_score = st.slider("Credit Score", 300, 850, 650)
            age = st.slider("Age", 18, 92, 40)
            tenure = st.slider("Tenure (Years)", 0, 10, 5)
            balance = st.number_input("Account Balance ($)", 0.0, 250000.0, 50000.0)
            
        with p_col2:
            num_of_products = st.selectbox("Number of Products", [1, 2, 3, 4])
            has_cr_card = st.selectbox("Has Credit Card?", [1, 0], format_func=lambda x: "Yes" if x == 1 else "No")
            is_active_member = st.selectbox("Is Active Member?", [1, 0], format_func=lambda x: "Yes" if x == 1 else "No")
            estimated_salary = st.number_input("Estimated Salary ($)", 0.0, 200000.0, 50000.0)

        submit_btn = st.form_submit_button("Calculate Churn Risk", type="primary")

    if submit_btn:
        # Placeholder for your model prediction logic:
        # e.g., input_data = [[credit_score, age, tenure, balance, ...]]
        # prediction = model.predict(input_data)
        
        st.success("Simulation Complete!")
        st.metric(label="Estimated Churn Probability", value="18.4%", delta="-3.2% vs baseline", delta_color="inverse")
        st.info("💡 Tip: Active members with more than 1 product generally show a significantly lower risk of churning.")


# TAB 3: RAW DATA & EXPORT
with tab3:
    st.subheader("Explore Filtered Dataset")
    st.markdown(f"Showing preview of {len(filtered_df):,} filtered rows.")
    
    # Safe interactive dataframe preview
    st.dataframe(filtered_df.head(100), use_container_width=True)
    
    # Safe Download Button
    st.download_button(
        label="📥 Download Filtered Data as CSV",
        data=filtered_df.to_csv(index=False).encode('utf-8'),
        file_name='filtered_european_bank_data.csv',
        mime='text/csv'
    )
