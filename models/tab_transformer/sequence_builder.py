import pandas as pd
import numpy as np


class SequenceBuilder:

    def __init__(
            self,
            sequence_length=20
    ):

        self.sequence_length = sequence_length

        self.feature_columns = [

            "amount",

            "merchant",

            "device",

            "country",

            "email_domain"
        ]

    def build_sequences(
            self,
            df
    ):

        X = []

        y = []

        grouped = df.groupby(
            "customer_id"
        )

        for customer_id, group in grouped:

            group = group.sort_values(
                "timestamp"
            )

            if len(group) <= self.sequence_length:

                continue

            features = group[
                self.feature_columns
            ]

            labels = group[
                "is_fraud"
            ]

            for i in range(

                self.sequence_length,

                len(group)

            ):

                sequence = (

                    features.iloc[
                        i-self.sequence_length:i
                    ]
                    .values
                )

                target = labels.iloc[i]

                X.append(
                    sequence
                )

                y.append(
                    target
                )

        X = np.array(X)

        y = np.array(y)

        return X, y