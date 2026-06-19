## Loads and merges raw data from the train_identity and train_transaction datasets
## Produces merged_dataset.parquet file as output and saved at data/interim

from pathlib import Path

import pandas as pd
import yaml


class DataLoader:

    def __init__(self, config_path: str = "configs/config.yaml"):
        self.config_path = config_path
        self.config = self.load_config()

    def load_config(self):

        with open(self.config_path, "r") as file:
            return yaml.safe_load(file)

    def load_raw_data(self):

        transaction_file = self.config["data"]["transaction_file"]
        identity_file = self.config["data"]["identity_file"]

        transaction_df = pd.read_csv(transaction_file)

        identity_df = pd.read_csv(identity_file)

        merged_df = transaction_df.merge(
            identity_df,
            on="TransactionID",
            how="left"
        )

        return merged_df

    def save_interim_dataset(
            self,
            df,
            output_path: str = "data/interim/merged_dataset.parquet"
    ):

        output_path = Path(output_path)

        output_path.parent.mkdir(
            parents=True,
            exist_ok=True
        )

        df.to_parquet(output_path, index=False)

        print(
            f"Dataset saved successfully at: {output_path}"
        )