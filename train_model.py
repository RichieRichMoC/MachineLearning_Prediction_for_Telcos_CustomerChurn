import pandas as pd
import numpy as np
from sklearn.preprocessing import StandardScaler, OneHotEncoder
from sklearn.compose import ColumnTransformer
from imblearn.pipeline import Pipeline
from imblearn.over_sampling import SMOTE
from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import RandomForestClassifier
from sklearn.impute import SimpleImputer
import joblib
import sys
import os

# Add current directory to path to import LogTransformer
sys.path.append(os.getcwd())
try:
    from log_transformer import LogTransformer
except ImportError:
    # Define LogTransformer if import fails (fallback)
    from sklearn.base import BaseEstimator, TransformerMixin
    class LogTransformer(BaseEstimator, TransformerMixin):
        def fit(self, X, y=None):
            return self
        def transform(self, X, y=None):
            return np.log1p(X)

def train_models():
    print("Loading data...")
    # Load data - assumes script is run from project root
    try:
        df = pd.read_csv('Dataset/Train.csv')
    except FileNotFoundError:
        print("Error: 'Dataset/Train.csv' not found. Please ensure you are in the project root.")
        return

    # Drop columns as per notebook analysis
    columns_to_drop = ['user_id', 'MRG', 'ZONE1', 'ZONE2', 'TOP_PACK']
    # Check if columns exist before dropping to avoid errors
    columns_to_drop = [c for c in columns_to_drop if c in df.columns]
    df = df.drop(columns=columns_to_drop)

    print("Data loaded and cleaned.")

    # Separate features and target
    if 'CHURN' not in df.columns:
        print("Error: Target column 'CHURN' not found.")
        return
        
    X = df.drop('CHURN', axis=1)
    y = df['CHURN']

    # Define features based on remaining columns
    # We infer numeric vs categorical based on dtypes or explicit list from analysis
    numeric_features = ['MONTANT', 'FREQUENCE_RECH', 'REVENUE', 'ARPU_SEGMENT', 'FREQUENCE', 
                        'DATA_VOLUME', 'ON_NET', 'ORANGE', 'TIGO', 'REGULARITY', 'FREQ_TOP_PACK']
    
    # Filter only those that actually exist in X
    numeric_features = [f for f in numeric_features if f in X.columns]
    
    categorical_features = ['REGION', 'TENURE']
    categorical_features = [f for f in categorical_features if f in X.columns]

    print(f"Numeric features: {numeric_features}")
    print(f"Categorical features: {categorical_features}")

    # Preprocessing pipelines
    numerical_transformer = Pipeline(steps=[
        ('imputer', SimpleImputer(strategy='mean')), # Mean imputation for numeric
        ('log', LogTransformer()),
        ('scaler', StandardScaler())
    ])

    categorical_transformer = Pipeline(steps=[
        ('imputer', SimpleImputer(strategy='most_frequent')), # Mode imputation for categorical
        ('encoder', OneHotEncoder(handle_unknown='ignore'))
    ])

    preprocessor = ColumnTransformer(
        transformers=[
            ('num', numerical_transformer, numeric_features),
            ('cat', categorical_transformer, categorical_features)
        ])

    # Models definition
    models = {
        'logistic_model': LogisticRegression(random_state=42, max_iter=1000),
        'random_forest_model': RandomForestClassifier(random_state=42, n_estimators=50, max_depth=10, n_jobs=-1)
    }

    # Ensure Models directory exists
    if not os.path.exists('Models'):
        os.makedirs('Models')

    # Train and save models
    for name, model in models.items():
        print(f"Training {name}...")
        pipeline = Pipeline(steps=[
            ('preprocessor', preprocessor),
            ('smote', SMOTE(random_state=42)),
            ('classifier', model)
        ])
        
        # Fit on full dataset for deployment model
        pipeline.fit(X, y)
        
        # Save model with compression to save space
        save_path = f'Models/{name}.joblib'
        joblib.dump(pipeline, save_path, compress=3)
        print(f"{name} saved to {save_path}.")

    print("All models training complete.")

if __name__ == "__main__":
    train_models()
