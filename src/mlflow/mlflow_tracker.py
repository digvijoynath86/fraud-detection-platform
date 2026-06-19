from pathlib import Path
import json
import yaml
import mlflow
import mlflow.xgboost
import joblib


class MLflowTracker:

    def __init__(self):

        self.model_path = (
            "models/xgboost_model.pkl"
        )

        self.metrics_path = (
            "artifacts/model_metrics.json"
        )

        self.threshold_path = (
            "artifacts/optimal_threshold.json"
        )

        self.feature_importance_path = (
            "artifacts/feature_importance.csv"
        )

        self.params_path = (
            "params.yaml"
        )

    def load_metrics(self):

        with open(
            self.metrics_path,
            "r"
        ) as f:

            return json.load(f)

    def load_threshold(self):

        with open(
            self.threshold_path,
            "r"
        ) as f:

            return json.load(f)

    def load_params(self):

        with open(
            self.params_path,
            "r"
        ) as f:

            return yaml.safe_load(f)

    def execute(self):

        metrics = self.load_metrics()

        threshold = self.load_threshold()

        params = self.load_params()

        model = joblib.load(
            self.model_path
        )

        mlflow.set_experiment(
            "Fraud Detection"
        )

        with mlflow.start_run(run_name=
    "xgboost_risk_features_v1"):

            # ------------------
            # Parameters
            # ------------------

            mlflow.log_param(
                "model_type",
                "xgboost"
            )

            mlflow.log_param(
                "max_depth",
                params["xgboost"]["max_depth"]
            )

            mlflow.log_param(
                "learning_rate",
                params["xgboost"]["learning_rate"]
            )

            mlflow.log_param(
                "n_estimators",
                params["xgboost"]["n_estimators"]
            )

            mlflow.log_param(
                "threshold",
                threshold["threshold"]
            )

            # ------------------
            # Metrics
            # ------------------

            for k, v in metrics.items():

                if isinstance(
                        v,
                        (int, float)
                ):

                    mlflow.log_metric(
                        k,
                        v
                    )

            # ------------------
            # Artifacts
            # ------------------

            mlflow.log_artifact(
                self.metrics_path
            )

            mlflow.log_artifact(
                self.threshold_path
            )

            if Path(
                    self.feature_importance_path
            ).exists():

                mlflow.log_artifact(
                    self.feature_importance_path
                )

            # ------------------
            # Model
            # ------------------

            mlflow.sklearn.log_model(
                model,
                artifact_path="model"
            )

            print(
                "MLflow logging completed."
            )