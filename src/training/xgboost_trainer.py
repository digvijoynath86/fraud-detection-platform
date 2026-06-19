from pathlib import Path
import yaml
import joblib
import pandas as pd

from xgboost import XGBClassifier


class XGBoostTrainer:

    def __init__(
            self,
            params_path="params.yaml"
    ):
        self.params = self.load_yaml(
            params_path
        )

    @staticmethod
    def load_yaml(path):

        with open(path, "r") as file:
            return yaml.safe_load(file)

    @staticmethod
    def load_data():

        X_train = pd.read_parquet(
            "data/risk_features/X_train_risk.parquet"
        )

        y_train = pd.read_parquet(
            "data/splits/y_train.parquet"
        )

        return (
            X_train,
            y_train.squeeze()
        )

    def train(self):

        X_train, y_train = (
            self.load_data()
        )
        fraud_count = y_train.sum()

        non_fraud_count = (
                len(y_train)
                - fraud_count
        )

        scale_pos_weight = (
                non_fraud_count
                / fraud_count
        )
        params = self.params["xgboost"]

        model = XGBClassifier(
            objective=params["objective"],
            max_depth=params["max_depth"],
            learning_rate=params[
                "learning_rate"
            ],
            n_estimators=params[
                "n_estimators"
            ],
            subsample=params[
                "subsample"
            ],
            colsample_bytree=params[
                "colsample_bytree"
            ],
            random_state=params[
                "random_state"
            ],
            eval_metric="auc",
            scale_pos_weight=scale_pos_weight
        )

        model.fit(
            X_train,
            y_train
        )

        return model

    @staticmethod
    def save_model(model):

        output_dir = Path(
            "models"
        )

        output_dir.mkdir(
            parents=True,
            exist_ok=True
        )

        joblib.dump(
            model,
            output_dir /
            "xgboost_model.pkl"
        )

    def execute(self):

        model = self.train()

        self.save_model(model)

        print(
            "Model training completed."
        )