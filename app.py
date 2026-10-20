import streamlit as st
import pandas as pd
import numpy as np

# Page Configuration
st.set_page_config(
    page_title="European Bank Churn Risk Dashboard",
    page_icon="🏦",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Gen Z Modern Executive Theme (Explicit Colors - Consistent across Light & Dark OS themes)
st.markdown("""
<style>
    /* Force high contrast text colors globally across OS theme switches */
    html, body, [class*="css"], .stMarkdown, p, span, label, div {
        color: #f3f4f6 !important;
        font-family: 'Inter', system-ui, -apple-system, sans-serif;
    }

    /* Main App Background: Deep Midnight Blue/Indigo Gradient */
    .stApp {
        background: radial-gradient(circle at 10% 20%, #111827 0%, #0f0a1e 50%, #030014 100%) !important;
    }

    /* Sidebar Background and Border */
    section[data-testid="stSidebar"] {
        background-color: #0b0918 !important;
        border-right: 1px solid rgba(139, 92, 246, 0.25) !important;
    }

    /* Sidebar Headers, Labels, Subheaders & Caption Override */
    section[data-testid="stSidebar"] h1,
    section[data-testid="stSidebar"] h2,
    section[data-testid="stSidebar"] h3,
    section[data-testid="stSidebar"] label,
    section[data-testid="stSidebar"] .stMarkdown,
    section[data-testid="stSidebar"] caption {
        color: #e2e8f0 !important;
    }

    /* Metric Cards Styling */
    div[data-testid="stMetric"] {
        background: rgba(22, 19, 43, 0.85) !important;
        border: 1px solid rgba(139, 92, 246, 0.3) !important;
        padding: 20px !important;
        border-radius: 16px !important;
        box-shadow: 0 8px 32px 0 rgba(0, 0, 0, 0.37) !important;
        backdrop-filter: blur(12px);
        -webkit-backdrop-filter: blur(12px);
        transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
        position: relative;
        overflow: hidden;
    }

    /* Hover Effect on Metric Cards */
    div[data-testid="stMetric"]:hover {
        transform: translateY(-4px);
        border-color: #38bdf8 !important;
        box-shadow: 0 12px 30px rgba(56, 189, 248, 0.25) !important;
    }

    /* Top Accent Line on Metric Cards */
    div[data-testid="stMetric"]::before {
        content: "";
        position: absolute;
        top: 0;
        left: 0;
        right: 0;
        height: 3px;
        background: linear-gradient(90deg, #a855f7, #38bdf8, #34d399);
    }

    /* KPI Titles / Labels inside Metric Cards */
    div[data-testid="stMetricLabel"], div[data-testid="stMetricLabel"] p {
        color: #cbd5e1 !important;
        font-weight: 600 !important;
        font-size: 0.95rem !important;
    }

    /* KPI Metric Values Color */
    div[data-testid="stMetricValue"], div[data-testid="stMetricValue"] div {
        color: #38bdf8 !important;
        font-weight: 700 !important;
    }

    /* Tab Headers */
    button[data-baseweb="tab"] {
        background-color: transparent !important;
        color: #9ca3af !important;
        font-weight: 600 !important;
        border-radius: 8px !important;
        padding: 8px 16px !important;
    }

    button[aria-selected="true"] {
        color: #ffffff !important;
        background: rgba(139, 92, 246, 0.3) !important;
        border-bottom: 2px solid #a855f7 !important;
    }

    /* Buttons: Purple/Blue Gradient */
    div.stButton > button, div.stDownloadButton > button {
        background: linear-gradient(135deg, #6366f1 0%, #a855f7 100%) !important;
        color: #ffffff !important;
        border-radius: 10px !important;
        border: none !important;
        padding: 10px 22px !important;
        font-weight: 600 !important;
        box-shadow: 0 4px 14px rgba(99, 102, 241, 0.35) !important;
    }

    div.stButton > button:hover, div.stDownloadButton > button:hover {
        background: linear-gradient(135deg, #4f46e5 0%, #9333ea 100%) !important;
        box-shadow: 0 6px 20px rgba(168, 85, 247, 0.5) !important;
    }
</style>
""", unsafe_allow_html=True)

# Load Data Safely from the 'data/' folder with a Fallback
@st.cache_data
def load_data():
    file_path = "data/European_Bank (1).csv"
    try:
        return pd.read_csv(file_path), True
    except FileNotFoundError:
        np.random.seed(42)
        n = 1000
        df_sample = pd.DataFrame({
            'CreditScore': np.random.randint(350, 850, n),
            'Geography': np.random.choice(['France', 'Spain', 'Germany'], n),
            'Gender': np.random.choice(['Female', 'Male'], n),
            'Age': np.random.randint(18, 70, n),
            'Balance': np.random.uniform(0, 150000, n),
            'Exited': np.random.choice([0, 1], n, p=[0.8, 0.2]),
            'Tenure': np.random.randint(0, 10, n),
            'NumOfProducts': np.random.randint(1, 4, n),
            'IsActiveMember': np.random.choice([0, 1], n),
            'EstimatedSalary': np.random.uniform(20000, 150000, n)
        })
        return df_sample, False

df, file_exists = load_data()

if not file_exists:
    st.warning("⚠️ 'data/European_Bank (1).csv' was not found. Displaying sample dashboard data.")

# --- SIDEBAR: Advanced Filters ---
st.sidebar.header("🔍 Advanced Filters")
st.sidebar.markdown("Slice and dice customer segments dynamically.")

countries = ["All"] + list(df['Geography'].unique()) if 'Geography' in df.columns else ["All"]
selected_country = st.sidebar.selectbox("Country", options=countries)

genders = ["All"] + list(df['Gender'].unique()) if 'Gender' in df.columns else ["All"]
selected_gender = st.sidebar.selectbox("Gender", options=genders)

min_age = int(df['Age'].min()) if 'Age' in df.columns else 18
max_age = int(df['Age'].max()) if 'Age' in df.columns else 100
age_range = st.sidebar.slider("Age Range", min_age, max_age, (min_age, max_age))

min_cs = int(df['CreditScore'].min()) if 'CreditScore' in df.columns else 300
max_cs = int(df['CreditScore'].max()) if 'CreditScore' in df.columns else 850
credit_range = st.sidebar.slider("Credit Score Range", min_cs, max_cs, (min_cs, max_cs))

activity_options = ["All", "Active Member", "Inactive Member"]
selected_activity = st.sidebar.selectbox("Activity Status", options=activity_options)

# Apply filters safely
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
st.markdown("Real-time customer risk intelligence, behavior analytics, and retention modeling.")
st.markdown("---")

# --- TOP METRICS ---
col1, col2, col3, col4 = st.columns(4)
col1.metric("Total Customers", f"{len(filtered_df):,}")
col2.metric("Avg Credit Score", int(filtered_df['CreditScore'].mean()) if 'CreditScore' in filtered_df.columns else 0)
col3.metric("Overall Churn Rate", f"{(filtered_df['Exited'].mean() * 100):.1f}%" if 'Exited' in filtered_df.columns else "0%")
col4.metric("Avg Balance", f"${filtered_df['Balance'].mean():,.2f}" if 'Balance' in filtered_df.columns else "$0.00")

st.markdown("---")

# --- TABS ---
tab1, tab2, tab3 = st.tabs(["📊 Overview & Insights", "🔮 Customer Simulator", "📁 Raw Data & Export"])

with tab1:
    st.subheader("📊 Customer Churn Insights & Trends")
    st.markdown("Analyze behavior patterns and risk factors within your filtered customer segment.")
    
    if len(filtered_df) == 0:
        st.warning("⚠️ No customers match your current filter criteria. Please adjust your sidebar filters.")
    else:
        if 'Exited' in filtered_df.columns:
            col_chart1, col_chart2 = st.columns(2)
            with col_chart1:
                st.markdown("**📍 Churn Rate by Country (%)**")
                if 'Geography' in filtered_df.columns:
                    geo_churn = filtered_df.groupby('Geography')['Exited'].mean() * 100
                    st.bar_chart(geo_churn)
            with col_chart2:
                st.markdown("**📈 Churn Rate by Age**")
                if 'Age' in filtered_df.columns:
                    age_churn = filtered_df.groupby('Age')['Exited'].mean() * 100
                    st.line_chart(age_churn)
                    
            st.markdown("---")
            col_chart3, col_chart4 = st.columns(2)
            with col_chart3:
                st.markdown("**👤 Impact of Active Membership (%)**")
                if 'IsActiveMember' in filtered_df.columns:
                    active_churn = filtered_df.groupby('IsActiveMember')['Exited'].mean() * 100
                    active_churn.index = active_churn.index.map({0: 'Inactive Member', 1: 'Active Member'})
                    st.bar_chart(active_churn)
            with col_chart4:
                st.markdown("**🛍️ Churn Rate by Number of Products**")
                if 'NumOfProducts' in filtered_df.columns:
                    prod_churn = filtered_df.groupby('NumOfProducts')['Exited'].mean() * 100
                    st.bar_chart(prod_churn)

with tab2:
    st.subheader("🔮 Individual Customer Churn Risk Simulator")
    st.markdown("Adjust customer attributes using the controls below to calculate their real-time churn probability.")

    with st.form("prediction_form"):
        p_col1, p_col2 = st.columns(2)
        with p_col1:
            credit_score = st.slider("Credit Score", 300, 850, 650)
            age = st.slider("Age", 18, 92, 40)
            tenure = st.slider("Tenure (Years)", 0, 10, 5)
            balance = st.number_input("Account Balance ($)", 0.0, 250000.0, 50000.0)
            geography = st.selectbox("Geography (Country)", ["France", "Germany", "Spain"])
        with p_col2:
            gender = st.selectbox("Gender", ["Female", "Male"])
            num_of_products = st.selectbox("Number of Bank Products", [1, 2, 3, 4])
            has_cr_card = st.selectbox("Has Credit Card?", [1, 0], format_func=lambda x: "Yes" if x == 1 else "No")
            is_active_member = st.selectbox("Is Active Member?", [1, 0], format_func=lambda x: "Yes" if x == 1 else "No")
            estimated_salary = st.number_input("Estimated Salary ($)", 0.0, 200000.0, 50000.0)

        submit_btn = st.form_submit_button("Calculate Churn Risk", type="primary")

    if submit_btn:
        input_dict = {
            'CreditScore': [credit_score], 'Age': [age], 'Tenure': [tenure], 'Balance': [balance],
            'NumOfProducts': [num_of_products], 'HasCrCard': [has_cr_card], 'IsActiveMember': [is_active_member],
            'EstimatedSalary': [estimated_salary], 'Geography': [geography], 'Gender': [gender]
        }
        input_df = pd.DataFrame(input_dict)
        
        risk_score = 0.10
        if age > 45: risk_score += 0.20
        if is_active_member == 0: risk_score += 0.15
        if geography == "Germany": risk_score += 0.15
        if num_of_products > 2: risk_score += 0.25
        if balance > 100000: risk_score += 0.05
        
        churn_prob = min(max(risk_score, 0.02), 0.95)
        
        st.markdown("---")
        st.subheader("Simulation Results")
        res_col1, res_col2 = st.columns(2)
        with res_col1:
            st.metric(label="Estimated Churn Probability", value=f"{churn_prob * 100:.1f}%", delta="High Risk" if churn_prob > 0.4 else "Low Risk", delta_color="inverse")
        with res_col2:
            if churn_prob > 0.4:
                st.error("⚠️ **High Risk Alert:** This customer exhibits strong indicators of churning. Consider offering a retention incentive.")
            else:
                st.success("✅ **Low Risk:** This customer is stable and likely to stay with the bank.")

with tab3:
    st.subheader("📁 Filtered Dataset View & Export")
    st.dataframe(filtered_df.head(100), use_container_width=True)
    st.download_button(
        "📥 Download Filtered Data as CSV",
        filtered_df.to_csv(index=False).encode('utf-8'),
        "filtered_bank_data.csv",
        "text/csv"
    )
