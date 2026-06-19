import joblib
import yaml
import json

class FraudPredictor:

    def __init__(
            self,
            model_path="models/xgboost_model.pkl",
            params_path="params.yaml"
    ):

        self.model = joblib.load(
            model_path
        )

        with open(
                params_path,
                "r"
        ) as file:

            self.params = yaml.safe_load(
                file
            )

        with open(
                "artifacts/optimal_threshold.json",
                "r"
        ) as file:
            threshold_config = json.load(
                file
            )

        self.threshold = (
            threshold_config["threshold"]
        )

    def predict(self, X):

        probabilities = (
            self.model.predict_proba(X)
            [:, 1]
        )

        predictions = (
            probabilities >= self.threshold
        ).astype(int)

        return predictions

    def predict_proba(self, X):

        return (
            self.model.predict_proba(X)
            [:, 1]
        )