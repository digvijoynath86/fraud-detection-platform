import numpy as np


class RealtimeFeatureBuilder:

    def build(

            self,

            transaction,

            history

    ):

        amounts = [

            txn["amount"]

            for txn in history
        ]

        avg_amount = (

            np.mean(amounts)

            if amounts

            else transaction["amount"]
        )

        max_amount = (

            np.max(amounts)

            if amounts

            else transaction["amount"]
        )

        features = {

            "amount_ratio":

                transaction["amount"]

                / (avg_amount + 1),

            "is_new_country":

                int(

                    any(

                        txn["country"]

                        != transaction["country"]

                        for txn in history
                    )
                ),

            "is_new_device":

                int(

                    any(

                        txn["device"]

                        != transaction["device"]

                        for txn in history
                    )
                ),

            "transaction_count":

                len(history),

            "avg_amount":

                avg_amount,

            "max_amount":

                max_amount
        }

        return features