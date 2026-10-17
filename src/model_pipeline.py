import pandas as pd
import numpy as np
import os
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler, OneHotEncoder
from sklearn.compose import ColumnTransformer
from sklearn.ensemble import RandomForestClassifier, GradientBoostingClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score, roc_auc_score

def load_and_preprocess_data(filepath=None):
    if filepath is None:
        # Automatically search root and current directory for ANY csv file
        root_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
        current_dir = os.path.dirname(__file__)
        
        search_dirs = [root_dir, current_dir, "."]
        csv_file = None
        
        for d in search_dirs:
            if os.path.exists(d):
                files = os.listdir(d)
                csv_files = [f for f in files if f.endswith('.csv')]
                if csv_files:
                    csv_file = os.path.join(d, csv_files[0])
                    break
        
        if csv_file is None:
            raise FileNotFoundError(f"No CSV dataset found in directories: {search_dirs}. Please ensure your dataset is uploaded to GitHub.")
        
        filepath = csv_file
            
    df = pd.read_csv(filepath)
    
    # 1. Feature Engineering
    df['BalanceToSalary'] = df['Balance'] / (df['EstimatedSalary'] + 1)
    df['ProductDensity'] = df['NumOfProducts'] / (df['Tenure'] + 1)
    df['AgeTenureRatio'] = df['Age'] / (df['Tenure'] + 1)
    df['IsActiveAndMultiProduct'] = ((df['IsActiveMember'] == 1) & (df['NumOfProducts'] > 1)).astype(int)
    
    # 2. Drop non-informative primary keys
    cols_to_drop = ['CustomerId', 'Surname']
    if 'Year' in df.columns:
        cols_to_drop.append('Year')
    df = df.drop(columns=cols_to_drop, errors='ignore')
    
    X = df.drop(columns=['Exited'])
    y = df['Exited']
    
    return train_test_split(X, y, test_size=0.2, random_state=42, stratify=y)

def train_and_evaluate_models(X_train, X_test, y_train, y_test):
    num_cols = ['CreditScore', 'Age', 'Tenure', 'Balance', 'NumOfProducts', 
                'EstimatedSalary', 'BalanceToSalary', 'ProductDensity', 'AgeTenureRatio']
    cat_cols = ['Geography', 'Gender']
    
    preprocessor = ColumnTransformer(
        transformers=[
            ('num', StandardScaler(), num_cols),
            ('cat', OneHotEncoder(drop='first'), cat_cols)
        ],
        remainder='passthrough'
    )
    
    X_train_prep = preprocessor.fit_transform(X_train)
    X_test_prep = preprocessor.transform(X_test)
    
    models = {
        'Logistic Regression': LogisticRegression(random_state=42),
        'Random Forest': RandomForestClassifier(n_estimators=100, random_state=42),
        'Gradient Boosting': GradientBoostingClassifier(n_estimators=100, random_state=42)
    }
    
    results = {}
    for name, model in models.items():
        model.fit(X_train_prep, y_train)
        preds = model.predict(X_test_prep)
        probs = model.predict_proba(X_test_prep)[:, 1]
        
        results[name] = {
            'Accuracy': accuracy_score(y_test, preds),
            'Precision': precision_score(y_test, preds),
            'Recall': recall_score(y_test, preds),
            'F1-Score': f1_score(y_test, preds),
            'ROC-AUC': roc_auc_score(y_test, probs),
            'model_object': model
        }
        
    return preprocessor, results
