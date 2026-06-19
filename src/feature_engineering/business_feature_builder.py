from pathlib import Path

import numpy as np
import pandas as pd


class BusinessFeatureBuilder:

    def __init__(
            self,
            input_path="data/processed/features.parquet",
            output_path="data/processed/business_features.parquet"
    ):
        self.input_path = input_path
        self.output_path = output_path

    def load_dataset(self):

        print(
            f"Loading dataset from {self.input_path}"
        )

        return pd.read_parquet(
            self.input_path
        )

    @staticmethod
    def create_amount_features(df):

        print(
            "Creating amount features..."
        )

        # Log transform
        df["amount_log"] = np.log1p(
            df["TransactionAmt"]
        )

        # Top 5% transactions
        threshold = (
            df["TransactionAmt"]
            .quantile(0.95)
        )

        df[
            "high_value_transaction"
        ] = (
            df["TransactionAmt"]
            > threshold
        ).astype(int)

        return df

    @staticmethod
    def create_customer_features(df):

        print(
            "Creating customer features..."
        )

        # card1 used as customer proxy
        customer_avg = (
            df.groupby("card1")
            ["TransactionAmt"]
            .transform("mean")
        )

        df[
            "customer_avg_amount"
        ] = customer_avg

        df["amount_ratio"] = (
            df["TransactionAmt"]
            /
            (
                df[
                    "customer_avg_amount"
                ] + 1
            )
        )

        return df

    # @staticmethod
    # def create_email_risk_score(df):
    #
    #     print(
    #         "Creating email domain risk score..."
    #     )
    #
    #     if (
    #             "P_emaildomain"
    #             not in df.columns
    #     ):
    #         print(
    #             "P_emaildomain not found."
    #         )
    #         return df
    #
    #     domain_risk = (
    #         df.groupby(
    #             "P_emaildomain"
    #         )["isFraud"]
    #         .mean()
    #     )
    #
    #     df[
    #         "email_domain_risk_score"
    #     ] = (
    #         df["P_emaildomain"]
    #         .map(domain_risk)
    #     )
    #
    #     return df

    # @staticmethod
    # def create_card_risk_score(df):
    #
    #     print(
    #         "Creating card risk score..."
    #     )
    #
    #     card_risk = (
    #         df.groupby("card1")
    #         ["isFraud"]
    #         .mean()
    #     )
    #
    #     df[
    #         "card_risk_score"
    #     ] = (
    #         df["card1"]
    #         .map(card_risk)
    #     )
    #
    #     return df

    @staticmethod
    def create_transaction_time_features(df):

        print(
            "Creating time features..."
        )

        if (
                "TransactionDT"
                not in df.columns
        ):
            print(
                "TransactionDT not found."
            )
            return df

        seconds_per_hour = 3600
        seconds_per_day = 86400

        df[
            "transaction_hour"
        ] = (
            df["TransactionDT"]
            // seconds_per_hour
        ) % 24

        df[
            "transaction_day"
        ] = (
            df["TransactionDT"]
            // seconds_per_day
        )

        df[
            "is_night_transaction"
        ] = (
            (
                df[
                    "transaction_hour"
                ] <= 5
            )
            |
            (
                df[
                    "transaction_hour"
                ] >= 23
            )
        ).astype(int)

        return df

    @staticmethod
    def remove_anonymous_features(df):

        columns_to_drop = [
            col
            for col in df.columns
            if col.startswith("V")
        ]

        print(
            f"Removing {len(columns_to_drop)} "
            f"anonymous V features"
        )

        return df.drop(
            columns=columns_to_drop
        )
    @staticmethod
    def save_dataset(df, output_path):

        output_path = Path(
            output_path
        )

        output_path.parent.mkdir(
            parents=True,
            exist_ok=True
        )

        df.to_parquet(
            output_path,
            index=False
        )

        print(
            f"Dataset saved to "
            f"{output_path}"
        )

    def execute(self):

        df = self.load_dataset()

        print(
            f"Initial Shape: {df.shape}"
        )

        df = self.create_amount_features(
            df
        )

        df = self.create_customer_features(
            df
        )

        # df = self.create_email_risk_score(
        #     df
        # )
        #
        # df = self.create_card_risk_score(
        #     df
        # )

        df = (
            self.create_transaction_time_features(
                df
            )
        )

        df = (
            self.remove_anonymous_features(
                df
            )
        )

        print(
            f"Final Shape: {df.shape}"
        )

        self.save_dataset(
            df,
            self.output_path
        )

        print(
            "Business feature engineering completed."
        )