import json
from pathlib import Path

import joblib
import pandas as pd
import numpy as np

from sklearn.metrics import (
    roc_auc_score,
    precision_score,
    recall_score,
    f1_score
)


class ModelEvaluator:

    @staticmethod
    def load_artifacts():

        model = joblib.load(
            "models/xgboost_model.pkl"
        )

        X_test = pd.read_parquet(
            "data/risk_features/X_test_risk.parquet"
        )

        y_test = pd.read_parquet(
            "data/splits/y_test.parquet"
        ).squeeze()

        return model, X_test, y_test


    def generate_threshold_analysis(
            self,
            model,
            X_test,
            y_test
    ):

        thresholds = np.arange(
            0.1,
            1.0,
            0.05
        )

        y_prob = model.predict_proba(
            X_test
        )[:, 1]

        results = []

        for threshold in thresholds:
            y_pred = (
                    y_prob >= threshold
            ).astype(int)

            precision = precision_score(
                y_test,
                y_pred,
                zero_division=0
            )

            recall = recall_score(
                y_test,
                y_pred,
                zero_division=0
            )

            f1 = f1_score(
                y_test,
                y_pred,
                zero_division=0
            )

            alerts_generated = int(
                y_pred.sum()
            )

            results.append(
                {
                    "threshold":
                        round(
                            float(threshold),
                            2
                        ),

                    "precision":
                        round(
                            precision,
                            4
                        ),

                    "recall":
                        round(
                            recall,
                            4
                        ),

                    "f1":
                        round(
                            f1,
                            4
                        ),

                    "alerts_generated":
                        alerts_generated
                }
            )

        return pd.DataFrame(results)
    def evaluate(self):

        model, X_test, y_test = (
            self.load_artifacts()
        )

        y_pred = model.predict(X_test)

        y_prob = model.predict_proba(
            X_test
        )[:, 1]

        metrics = {

            "auc": float(
                roc_auc_score(
                    y_test,
                    y_prob
                )
            ),

            "precision": float(
                precision_score(
                    y_test,
                    y_pred
                )
            ),

            "recall": float(
                recall_score(
                    y_test,
                    y_pred
                )
            ),

            "f1": float(
                f1_score(
                    y_test,
                    y_pred
                )
            )
        }

        return metrics

    @staticmethod
    def save_metrics(metrics):

        output_dir = Path(
            "artifacts"
        )

        output_dir.mkdir(
            parents=True,
            exist_ok=True
        )

        with open(
            output_dir /
            "model_metrics.json",
            "w"
        ) as file:

            json.dump(
                metrics,
                file,
                indent=4
            )

    @staticmethod
    def save_threshold_analysis(df):

        output_dir = Path(
            "artifacts"
        )

        output_dir.mkdir(
            parents=True,
            exist_ok=True
        )

        output_file = (
                output_dir /
                "threshold_metrics.csv"
        )

        df.to_csv(
            output_file,
            index=False
        )

        print(
            f"Threshold report saved to "
            f"{output_file}"
        )

    @staticmethod
    def save_optimal_threshold(threshold_df):

        best_row = (
            threshold_df
            .sort_values(
                by="f1",
                ascending=False
            )
            .iloc[0]
        )

        optimal_threshold = {

            "threshold": float(
                best_row["threshold"]
            ),

            "precision": float(
                best_row["precision"]
            ),

            "recall": float(
                best_row["recall"]
            ),

            "f1": float(
                best_row["f1"]
            ),

            "alerts_generated": int(
                best_row["alerts_generated"]
            )
        }

        output_dir = Path(
            "artifacts"
        )

        output_dir.mkdir(
            parents=True,
            exist_ok=True
        )

        output_file = (
                output_dir /
                "optimal_threshold.json"
        )

        with open(
                output_file,
                "w"
        ) as file:
            json.dump(
                optimal_threshold,
                file,
                indent=4
            )

        print(
            f"Optimal threshold saved to "
            f"{output_file}"
        )

        print(
            "\nSelected Threshold:"
        )

        print(
            json.dumps(
                optimal_threshold,
                indent=4
            )
        )
    def execute(self):

        metrics = self.evaluate()

        self.save_metrics(metrics)

        print("\nModel Metrics")

        for k, v in metrics.items():

            print(
                f"{k}: {v:.4f}"
            )

        model, X_test, y_test = (
            self.load_artifacts()
        )

        threshold_df = (
            self.generate_threshold_analysis(
                model,
                X_test,
                y_test
            )
        )

        self.save_threshold_analysis(
            threshold_df
        )

        self.save_optimal_threshold(
            threshold_df
        )

        print(
            "\nTop Thresholds by F1:"
        )

        print(
            threshold_df
            .sort_values(
                by="f1",
                ascending=False
            )
            .head(10)
        )