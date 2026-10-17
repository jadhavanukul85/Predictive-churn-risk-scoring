# Predictive Modeling and Risk Scoring for Bank Customer Churn: A Machine Learning Framework for Retail Banking

**Author:** Anukul Jadhav  
**Target Organization:** Unified Mentor / European Banking Regulatory Analytics Framework  

---

## Abstract
Traditional retail banking churn analysis relies on retrospective behavioral metrics that explain past account closures rather than predicting future attrition. This study introduces an advanced predictive machine learning framework designed to calculate continuous individual customer churn risk probabilities (0% to 100%) prior to account termination. Evaluating 10,000 retail banking client records across Germany, France, and Spain, we benchmark Logistic Regression, Random Forest, and Gradient Boosting classifiers. Our models incorporate advanced feature engineering—including balance-to-salary ratios, product density indicators, and age-tenure interaction terms—to achieve superior ROC-AUC performance and enable proactive, targeted customer retention.

---

## 1. Introduction & Business Motivation
Customer lifetime value (CLV) and revenue stability depend heavily on active deposit retention. Acquiring new retail banking clients costs 5 to 7 times more than retaining existing relationships. While exploratory data analysis identifies aggregate risk trends, modern banking governance requires real-time predictive scoring to:
* **Transition from Reactive to Proactive:** Identify customers exhibiting early warning signals before they initiate account closure.
* **Optimize Retention Expenditure:** Target incentive offers specifically to high-risk clients rather than broad, costly campaigns.
* **Ensure Regulatory Compliance:** Provide explainable risk scores that align with European Central Bank (ECB) risk management standards.

---

## 2. Methodology & Feature Engineering
The modeling pipeline processes customer records through rigorous data preprocessing and feature creation:
1. **Identifier Removal:** Dropped non-informative fields (`CustomerId`, `Surname`) to prevent overfitting and ensure privacy compliance.
2. **Advanced Feature Engineering:**
   * **`BalanceToSalary`:** Ratio of account balance to estimated annual income, assessing capital exposure relative to earnings.
   * **`ProductDensity`:** Number of active bank products divided by account tenure, quantifying product bundling intensity.
   * **`AgeTenureRatio`:** Interaction term between client age and years with the institution.
   * **`IsActiveAndMultiProduct`:** Binary interaction flag identifying active multi-product engagement.
3. **Train-Test Split:** Executed a stratified 80/20 train-test split preserving the minority churn class distribution (~20.37%).

---

## 3. Model Evaluation & Performance Benchmarking
Three classification algorithms were trained and evaluated on test data:
* **Logistic Regression:** Baseline linear model providing high coefficient interpretability.
* **Random Forest Classifier:** Ensemble bagging model capturing non-linear feature interactions.
* **Gradient Boosting Classifier:** Sequential boosting model optimized for predictive accuracy and recall.

### Evaluation Metrics Summary:
* **Recall:** Prioritized to ensure the model captures the maximum possible actual churners, minimizing false negatives.
* **ROC-AUC:** Demonstrates robust classification discrimination across probability thresholds.

---

## 4. Strategic Recommendations & Risk Mitigation
1. **Automated Risk Scoring Integration:** Embed real-time churn probability scoring directly into core banking CRMs.
2. **Targeted Interventions for High-Probability Segments:** Trigger automated relationship manager outreach when customer risk scores exceed 50%.
3. **Product Unbundling Reviews:** Address structural friction identified in multi-product accounts holding 3+ products.
