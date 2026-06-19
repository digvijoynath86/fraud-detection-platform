from pathlib import Path

import pandas as pd


class VelocityFeatureBuilder:

    def __init__(
            self,
            input_path="data/processed/business_features.parquet",
            output_path="data/processed/velocity_features.parquet"
    ):
        self.input_path = input_path
        self.output_path = output_path

    def load_dataset(self):

        return pd.read_parquet(
            self.input_path
        )

    @staticmethod
    def create_velocity_features(df):

        print(
            "Creating velocity features..."
        )

        df = df.sort_values(
            ["card1", "TransactionDT"]
        )

        # Previous transactions count

        df["txn_count_customer"] = (
            df.groupby("card1")
            .cumcount()
        )

        # Running average amount

        df["avg_amount_customer"] = (
            df.groupby("card1")
            ["TransactionAmt"]
            .expanding()
            .mean()
            .reset_index(
                level=0,
                drop=True
            )
        )

        # Running max amount

        df["max_amount_customer"] = (
            df.groupby("card1")
            ["TransactionAmt"]
            .expanding()
            .max()
            .reset_index(
                level=0,
                drop=True
            )
        )

        return df

    def save_dataset(self, df):

        output_path = Path(
            self.output_path
        )

        output_path.parent.mkdir(
            parents=True,
            exist_ok=True
        )

        df.to_parquet(
            output_path,
            index=False
        )

    def execute(self):

        df = self.load_dataset()

        print(
            f"Initial Shape: {df.shape}"
        )

        df = self.create_velocity_features(
            df
        )

        print(
            f"Final Shape: {df.shape}"
        )

        self.save_dataset(df)

        print(
            "Velocity features created."
        )