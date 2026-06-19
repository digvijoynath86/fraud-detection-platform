import torch

import torch.nn as nn


class TabTransformer(

    nn.Module

):

    def __init__(

            self,

            num_numeric=1,

            num_categories=None,

            embedding_dim=32,

            num_heads=4,

            num_layers=2,

            dropout=0.2

    ):

        super().__init__()

        self.embedding_dim = embedding_dim

        self.num_categories = len(

            num_categories
        )

        # Numeric feature projection

        self.numeric_projection = (

            nn.Linear(

                num_numeric,

                embedding_dim
            )
        )

        # Embeddings for categorical features

        self.category_embeddings = (

            nn.ModuleList(

                [

                    nn.Embedding(

                        cardinality,

                        embedding_dim

                    )

                    for cardinality

                    in num_categories
                ]
            )
        )

        # Project concatenated features

        total_features = (

            self.num_categories + 1

        ) * embedding_dim

        self.feature_projection = (

            nn.Linear(

                total_features,

                embedding_dim
            )
        )

        # Transformer encoder

        encoder_layer = (

            nn.TransformerEncoderLayer(

                d_model=embedding_dim,

                nhead=num_heads,

                dropout=dropout,

                batch_first=True
            )
        )

        self.transformer = (

            nn.TransformerEncoder(

                encoder_layer,

                num_layers=num_layers
            )
        )

        # Classifier

        self.classifier = (

            nn.Sequential(

                nn.Linear(

                    embedding_dim,

                    64
                ),

                nn.ReLU(),

                nn.Dropout(

                    dropout
                ),

                nn.Linear(

                    64,

                    1
                ),

                nn.Sigmoid()
            )
        )

    def forward(

            self,

            x_numeric,

            x_categorical

    ):

        # Numeric

        numeric = (

            self.numeric_projection(

                x_numeric
            )
        )

        # Categorical

        categorical = []

        for i, embedding in enumerate(

                self.category_embeddings

        ):

            categorical.append(

                embedding(

                    x_categorical[:, :, i]

                )
            )

        # Combine all features

        x = torch.cat(

            [numeric] + categorical,

            dim=-1
        )

        # Transaction embedding

        x = self.feature_projection(

            x
        )

        # Self-attention

        x = self.transformer(

            x
        )

        # Use last transaction

        x = x[:, -1, :]

        return self.classifier(

            x
        )