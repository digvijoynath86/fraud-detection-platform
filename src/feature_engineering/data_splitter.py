## To create train test split
## Test size and random state will be fetched from params.yaml
## Output - X_train.parquet,X_test.parquet,y_train.parquet, y_test.parquet, split_metadata.json
import json
from pathlib import Path

import pandas as pd
import yaml
from sklearn.model_selection import train_test_split


class DataSplitter:

    def __init__(
            self,
            params_path="params.yaml"
    ):
        self.params = self._load_yaml(
            params_path
        )

    @staticmethod
    def _load_yaml(path):

        with open(path, "r") as file:
            return yaml.safe_load(file)

    @staticmethod
    def load_features():

        return pd.read_parquet(
            "data/processed/velocity_features.parquet"
        )

    def split_data(self):

        df = self.load_features()

        X = df.drop(
            columns=["isFraud"]
        )

        y = df["isFraud"]

        X_train, X_test, y_train, y_test = (
            train_test_split(
                X,
                y,
                test_size=self.params[
                    "data_split"
                ]["test_size"],
                random_state=self.params[
                    "data_split"
                ]["random_state"],
                stratify=y
            )
        )

        return (
            X_train,
            X_test,
            y_train,
            y_test
        )

    @staticmethod
    def save_split_data(
            X_train,
            X_test,
            y_train,
            y_test
    ):

        output_dir = Path(
            "data/splits"
        )

        output_dir.mkdir(
            parents=True,
            exist_ok=True
        )

        X_train.to_parquet(
            output_dir /
            "X_train.parquet",
            index=False
        )

        X_test.to_parquet(
            output_dir /
            "X_test.parquet",
            index=False
        )

        y_train.to_frame().to_parquet(
            output_dir /
            "y_train.parquet",
            index=False
        )

        y_test.to_frame().to_parquet(
            output_dir /
            "y_test.parquet",
            index=False
        )

    @staticmethod
    def save_metadata(
            X_train,
            X_test,
            y_train,
            y_test
    ):

        metadata = {

            "train_rows":
                int(len(X_train)),

            "test_rows":
                int(len(X_test)),

            "train_fraud_rate":
                float(y_train.mean()),

            "test_fraud_rate":
                float(y_test.mean())
        }

        output_path = Path(
            "artifacts/split_metadata.json"
        )

        output_path.parent.mkdir(
            parents=True,
            exist_ok=True
        )

        with open(
                output_path,
                "w"
        ) as file:

            json.dump(
                metadata,
                file,
                indent=4
            )

    def execute(self):

        (
            X_train,
            X_test,
            y_train,
            y_test
        ) = self.split_data()

        self.save_split_data(
            X_train,
            X_test,
            y_train,
            y_test
        )

        self.save_metadata(
            X_train,
            X_test,
            y_train,
            y_test
        )

        print(
            f"Train Shape: "
            f"{X_train.shape}"
        )

        print(
            f"Test Shape: "
            f"{X_test.shape}"
        )