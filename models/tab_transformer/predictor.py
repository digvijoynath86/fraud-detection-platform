from pathlib import Path

import joblib
import numpy as np

import torch

from models.tab_transformer.model import (
    TabTransformer
)


class TabTransformerPredictor:

    def __init__(self):

        self.device = (

            "cuda"

            if torch.cuda.is_available()

            else "cpu"
        )

        self.label_encoders = (

            joblib.load(

                "models/label_encoders.pkl"
            )
        )

        cardinalities = []

        for encoder in (

            self.label_encoders.values()

        ):

            cardinalities.append(

                len(

                    encoder.classes_
                )
            )

        self.model = (

            TabTransformer(

                num_numeric=1,

                num_categories=cardinalities
            )
        )

        self.model.load_state_dict(

            torch.load(

                "models/tab_transformer.pth",

                map_location=self.device
            )
        )

        self.model.eval()

    def predict(

            self,

            history

    ):

        if len(history) < 20:

            return 0.0

        history = history[-20:]

        numeric = []

        categorical = []

        for txn in history:

            numeric.append([

                txn["amount"]

            ])

            categorical.append([

                self.label_encoders[
                    "merchant"
                ].transform(

                    [txn["merchant"]]

                )[0],

                self.label_encoders[
                    "device"
                ].transform(

                    [txn["device"]]

                )[0],

                self.label_encoders[
                    "country"
                ].transform(

                    [txn["country"]]

                )[0],

                self.label_encoders[
                    "email_domain"
                ].transform(

                    [txn["email_domain"]]

                )[0]
            ])

        x_numeric = (

            torch.tensor(

                [numeric]

            )

            .float()

            .to(self.device)
        )

        x_categorical = (

            torch.tensor(

                [categorical]

            )

            .long()

            .to(self.device)
        )

        with torch.no_grad():

            score = (

                self.model(

                    x_numeric,

                    x_categorical
                )

                .item()
            )

        return round(

            score,

            4
        )