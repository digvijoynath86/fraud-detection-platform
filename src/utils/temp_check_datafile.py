import joblib
import pandas as pd
from src.kafka.transaction_generator import (
    TransactionGenerator
)

def get_feature_importance():
    model = joblib.load(
        "models/xgboost_model.pkl"
    )
    X_train = pd.read_parquet(
        "data/risk_features/X_train_risk.parquet"
    )

    # Read the Parquet file
    df = pd.read_parquet('data/risk_features/X_test_risk.parquet')

    # Display the first few rows
    print(df.head())

    feature_importance = pd.DataFrame(
        {
            "feature": X_train.columns,
            "importance": model.feature_importances_
        }
    )

    print(
        feature_importance
        .sort_values(
            by="importance",
            ascending=False
        )
        .head(30)
    )

def check_dataset(input_file):
    df = pd.read_parquet(
        input_file
    )

    print(
        df["TransactionDT"].describe()
    )
def generate_transaction_data():
    generator = (
        TransactionGenerator()
    )

    print(
        generator.generate_transaction()
    )
##get_feature_importance()
#check_dataset("data/processed/business_features.parquet")
generate_transaction_data()