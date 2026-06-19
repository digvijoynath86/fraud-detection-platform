from pathlib import Path

import joblib
import mlflow

import numpy as np
import pandas as pd

import torch

from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder

from torch.utils.data import (
    DataLoader,
    TensorDataset
)

from models.tab_transformer.model import (
    TabTransformer
)

import torch.nn as nn

from sklearn.metrics import (
    roc_auc_score,
    precision_score,
    recall_score,
    f1_score
)

from pathlib import Path


class TabTransformerTrainer:

    def __init__(

            self,

            sequence_length=20,

            batch_size=64,

            epochs=10,

            learning_rate=0.001

    ):

        self.sequence_length = (
            sequence_length
        )

        self.batch_size = (
            batch_size
        )

        self.epochs = epochs

        self.learning_rate = (
            learning_rate
        )

        self.categorical_features = [

            "merchant",

            "device",

            "country",

            "email_domain"
        ]

        self.numeric_features = [

            "amount"
        ]

        self.label_encoders = {}

        self.model = None

    def load_data(self):
        df = pd.read_parquet(

            "data/processed/synthetic_transactions.parquet"

        )

        df = df.sort_values(

            ["customer_id", "timestamp"]

        )

        return df

    def encode_features(

            self,

            df

    ):
        for column in self.categorical_features:
            encoder = LabelEncoder()

            df[column] = (

                encoder.fit_transform(

                    df[column]
                )
            )

            self.label_encoders[
                column
            ] = encoder

        return df

    def create_sequences(

            self,

            df

    ):

        X_numeric = []

        X_categorical = []

        y = []

        grouped = df.groupby(

            "customer_id"
        )

        for _, group in grouped:

            if len(group) <= self.sequence_length:
                continue

            for i in range(

                    self.sequence_length,

                    len(group)

            ):
                sequence = (

                    group.iloc[
                    i - self.sequence_length:i
                    ]
                )

                X_numeric.append(

                    sequence[
                        self.numeric_features
                    ].values
                )

                X_categorical.append(

                    sequence[
                        self.categorical_features
                    ].values
                )

                y.append(

                    group.iloc[i][
                        "is_fraud"
                    ]
                )

        return (

            np.array(X_numeric),

            np.array(X_categorical),

            np.array(y)
        )

    def create_dataloaders(

            self,

            X_numeric,

            X_categorical,

            y

    ):

        Xn_train, Xn_test, \
 \
            Xc_train, Xc_test, \
 \
            y_train, y_test = (

            train_test_split(

                X_numeric,

                X_categorical,

                y,

                test_size=0.2,

                stratify=y,

                random_state=42
            )
        )

        train_dataset = TensorDataset(

            torch.tensor(
                Xn_train
            ).float(),

            torch.tensor(
                Xc_train
            ).long(),

            torch.tensor(
                y_train
            ).float()
        )

        test_dataset = TensorDataset(

            torch.tensor(
                Xn_test
            ).float(),

            torch.tensor(
                Xc_test
            ).long(),

            torch.tensor(
                y_test
            ).float()
        )

        return (

            DataLoader(

                train_dataset,

                batch_size=self.batch_size,

                shuffle=True
            ),

            DataLoader(

                test_dataset,

                batch_size=self.batch_size
            )
        )

    def train(
            self,
            train_loader,
            test_loader
    ):

        device = (

            "cuda"

            if torch.cuda.is_available()

            else "cpu"
        )

        print(f"Using {device}")

        cardinalities = []

        for column in self.categorical_features:
            cardinalities.append(

                len(

                    self.label_encoders[
                        column
                    ].classes_
                )
            )

        self.model = TabTransformer(

            num_numeric=1,

            num_categories=cardinalities
        )

        self.model.to(device)

        criterion = nn.BCELoss()

        optimizer = torch.optim.Adam(

            self.model.parameters(),

            lr=self.learning_rate
        )

        mlflow.start_run()

        mlflow.log_params({

            "sequence_length":

                self.sequence_length,

            "epochs":

                self.epochs,

            "batch_size":

                self.batch_size,

            "learning_rate":

                self.learning_rate
        })

        for epoch in range(

                self.epochs

        ):

            self.model.train()

            total_loss = 0

            for (

                    x_numeric,

                    x_categorical,

                    y

            ) in train_loader:
                x_numeric = x_numeric.to(
                    device
                )

                x_categorical = (

                    x_categorical.to(
                        device
                    )
                )

                y = y.to(
                    device
                )

                optimizer.zero_grad()

                predictions = (

                    self.model(

                        x_numeric,

                        x_categorical
                    )

                    .squeeze()
                )

                loss = criterion(

                    predictions,

                    y
                )

                loss.backward()

                optimizer.step()

                total_loss += (

                    loss.item()
                )

            avg_loss = (

                    total_loss

                    / len(train_loader)
            )

            print(

                f"Epoch "

                f"{epoch + 1}/{self.epochs}"

                f" Loss={avg_loss:.4f}"
            )

        mlflow.log_metric(

            "train_loss",

            avg_loss
        )

        self.evaluate(
            test_loader
        )

    def evaluate(
            self,
            test_loader
    ):

        device = (

            "cuda"

            if torch.cuda.is_available()

            else "cpu"
        )

        self.model.eval()

        predictions = []

        actuals = []

        with torch.no_grad():

            for (

                    x_numeric,

                    x_categorical,

                    y

            ) in test_loader:
                x_numeric = x_numeric.to(
                    device
                )

                x_categorical = (

                    x_categorical.to(
                        device
                    )
                )

                outputs = (

                    self.model(

                        x_numeric,

                        x_categorical
                    )

                    .squeeze()

                    .cpu()

                    .numpy()
                )

                predictions.extend(
                    outputs
                )

                actuals.extend(
                    y.numpy()
                )

        predictions = np.array(
            predictions
        )

        actuals = np.array(
            actuals
        )
        print("\nPrediction Distribution")

        print(pd.Series(predictions).describe())

        print("\nTop 20 Predictions")

        print(

            sorted(

                predictions,

                reverse=True

            )[:20]
        )
        predicted_labels = (

                predictions >= 0.5
        )

        metrics = {

            "auc":

                roc_auc_score(

                    actuals,

                    predictions
                ),

            "precision":

                precision_score(

                    actuals,

                    predicted_labels
                ),

            "recall":

                recall_score(

                    actuals,

                    predicted_labels
                ),

            "f1":

                f1_score(

                    actuals,

                    predicted_labels
                )
        }

        for k, v in metrics.items():
            print(

                f"{k}: "

                f"{v:.4f}"
            )

            mlflow.log_metric(
                k,
                v
            )

        self.save_model()

        mlflow.end_run()

    def save_model(self):

        output_dir = Path(
            "models"
        )

        output_dir.mkdir(
            exist_ok=True
        )

        torch.save(

            self.model.state_dict(),

            output_dir

            / "tab_transformer.pth"
        )

        joblib.dump(

            self.label_encoders,

            output_dir

            / "label_encoders.pkl"
        )

        print(
            "Model saved."
        )

    def execute(self):

        df = self.load_data()

        df = self.encode_features(
            df
        )

        Xn, Xc, y = (

            self.create_sequences(
                df
            )
        )

        train_loader, test_loader = (

            self.create_dataloaders(

                Xn,

                Xc,

                y
            )
        )

        self.train(

            train_loader,

            test_loader
        )
if __name__ == "__main__":

    trainer = (

        TabTransformerTrainer()

    )

    trainer.execute()

trainer = TabTransformerTrainer()

df = trainer.load_data()

df = trainer.encode_features(df)

Xn, Xc, y = trainer.create_sequences(df)

print(Xn.shape)

print(Xc.shape)

print(y.shape)