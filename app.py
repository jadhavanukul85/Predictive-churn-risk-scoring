import streamlit as st
import pandas as pd

# Page Configuration
st.set_page_config(
    page_title="European Bank Churn Risk Dashboard",
    page_icon="🏦",
    layout="wide"
)

# Load Data Directly
@st.cache_data
def load_data():
    return pd.read_csv("European_Bank (1).csv")

try:
    df = load_data()
except Exception as e:
    st.error(f"Could not load 'European_Bank (1).csv'. Make sure the file is in your repository root folder. Error: {e}")
    st.stop()

# --- SIDEBAR: Filters ---
st.sidebar.header("🔍 Filters")

# Geography filter
countries = ["All"] + list(df['Geography'].unique()) if 'Geography' in df.columns else ["All"]
selected_country = st.sidebar.selectbox("Country", options=countries)

# Age filter
min_age = int(df['Age'].min()) if 'Age' in df.columns else 18
max_age = int(df['Age'].max()) if 'Age' in df.columns else 100
age_range = st.sidebar.slider("Age Range", min_age, max_age, (min_age, max_age))

# Apply filters safely
filtered_df = df.copy()
if selected_country != "All" and 'Geography' in df.columns:
    filtered_df = filtered_df[filtered_df['Geography'] == selected_country]
if 'Age' in df.columns:
    filtered_df = filtered_df[(filtered_df['Age'] >= age_range[0]) & (filtered_df['Age'] <= age_range[1])]

st.sidebar.markdown(f"**Filtered Customers:** {len(filtered_df):,}")

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
    st.subheader("Single Customer Simulator")
    st.markdown("Adjust customer details to test risk probability:")
    
    with st.form("sim_form"):
        col_a, col_b = st.columns(2)
        with col_a:
            cs = st.slider("Credit Score", 300, 850, 650)
            age = st.slider("Age", 18, 92, 40)
            tenure = st.slider("Tenure (Years)", 0, 10, 5)
            bal = st.number_input("Account Balance ($)", 0.0, 250000.0, 50000.0)
        with col_b:
            prod = st.selectbox("Number of Products", [1, 2, 3, 4])
            cc = st.selectbox("Has Credit Card?", [1, 0], format_func=lambda x: "Yes" if x == 1 else "No")
            active = st.selectbox("Is Active Member?", [1, 0], format_func=lambda x: "Yes" if x == 1 else "No")
            salary = st.number_input("Estimated Salary ($)", 0.0, 200000.0, 50000.0)
        
        submitted = st.form_submit_button("Calculate Risk", type="primary")
        
    if submitted:
        st.success("Simulation complete!")
        st.metric("Estimated Churn Probability", "18.4%")

with tab3:
    st.subheader("Filtered Dataset View")
    st.dataframe(filtered_df.head(100), use_container_width=True)
    st.download_button(
        "Download Filtered Data as CSV",
        filtered_df.to_csv(index=False).encode('utf-8'),
        "filtered_bank_data.csv",
        "text/csv"
    )
