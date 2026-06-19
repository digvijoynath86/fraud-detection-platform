from pathlib import Path

import pandas as pd

from src.services.transaction_service.customer_profile_generator import (
    CustomerProfileGenerator
)

from src.services.transaction_service.transaction_generator import (
    TransactionGenerator
)


class DatasetBuilder:

    def __init__(

            self,

            n_customers=1000,

            transactions_per_customer=100

    ):

        self.n_customers = n_customers

        self.transactions_per_customer = (
            transactions_per_customer
        )

        self.profile_generator = (
            CustomerProfileGenerator()
        )

        self.transaction_generator = (
            TransactionGenerator()
        )

    def build_dataset(self):

        profiles = (

            self.profile_generator.generate_profiles(

                n_customers=self.n_customers
            )
        )

        dataset = []

        for customer_id, profile in profiles.items():

            for _ in range(

                self.transactions_per_customer

            ):

                transaction = (

                    self.transaction_generator.generate_transaction(

                        customer_id,

                        profile
                    )
                )

                dataset.append(
                    transaction
                )

        return pd.DataFrame(
            dataset
        )

    def save_dataset(

            self,

            df

    ):

        output_path = Path(

            "data/processed/synthetic_transactions.parquet"

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

        df = self.build_dataset()

        print(

            f"Dataset Shape: {df.shape}"

        )

        self.save_dataset(df)

        print(

            "Synthetic dataset saved."

        )