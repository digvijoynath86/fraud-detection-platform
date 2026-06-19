from pathlib import Path

import pandas as pd


class RiskFeatureBuilder:

    def __init__(self):

        self.train_path = (
            "data/splits/X_train.parquet"
        )

        self.test_path = (
            "data/splits/X_test.parquet"
        )

        self.y_train_path = (
            "data/splits/y_train.parquet"
        )

        self.output_dir = (
            "data/risk_features"
        )

    def load_data(self):

        X_train = pd.read_parquet(
            self.train_path
        )

        X_test = pd.read_parquet(
            self.test_path
        )

        y_train = (
            pd.read_parquet(
                self.y_train_path
            )
            .squeeze()
        )

        return (
            X_train,
            X_test,
            y_train
        )

    @staticmethod
    def create_card_risk_table(
            X_train,
            y_train
    ):

        train_df = X_train.copy()

        train_df["isFraud"] = y_train

        return (
            train_df
            .groupby("card1")
            ["isFraud"]
            .mean()
        )

    @staticmethod
    def create_email_risk_table(
            X_train,
            y_train
    ):

        train_df = X_train.copy()

        train_df["isFraud"] = y_train

        return (
            train_df
            .groupby(
                "P_emaildomain"
            )
            ["isFraud"]
            .mean()
        )

    @staticmethod
    def apply_card_risk(
            df,
            risk_table
    ):

        global_mean = (
            risk_table.mean()
        )

        df[
            "card_risk_score"
        ] = (
            df["card1"]
            .map(risk_table)
            .fillna(global_mean)
        )

        return df

    @staticmethod
    def apply_email_risk(
            df,
            risk_table
    ):

        global_mean = (
            risk_table.mean()
        )

        df[
            "email_domain_risk_score"
        ] = (
            df[
                "P_emaildomain"
            ]
            .map(risk_table)
            .fillna(global_mean)
        )

        return df

    def execute(self):

        (
            X_train,
            X_test,
            y_train
        ) = self.load_data()

        card_risk_table = (
            self.create_card_risk_table(
                X_train,
                y_train
            )
        )

        email_risk_table = (
            self.create_email_risk_table(
                X_train,
                y_train
            )
        )

        X_train = (
            self.apply_card_risk(
                X_train,
                card_risk_table
            )
        )

        X_test = (
            self.apply_card_risk(
                X_test,
                card_risk_table
            )
        )

        X_train = (
            self.apply_email_risk(
                X_train,
                email_risk_table
            )
        )

        X_test = (
            self.apply_email_risk(
                X_test,
                email_risk_table
            )
        )

        output_dir = Path(
            self.output_dir
        )

        output_dir.mkdir(
            parents=True,
            exist_ok=True
        )

        X_train.to_parquet(
            output_dir /
            "X_train_risk.parquet",
            index=False
        )

        X_test.to_parquet(
            output_dir /
            "X_test_risk.parquet",
            index=False
        )

        print(
            "Risk features created."
        )