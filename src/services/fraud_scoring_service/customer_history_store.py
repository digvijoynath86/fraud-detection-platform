from collections import defaultdict, deque


class CustomerHistoryStore:

    def __init__(

            self,

            history_size=50

    ):

        self.history_size = history_size

        self.customer_history = defaultdict(

            lambda: deque(

                maxlen=self.history_size
            )
        )

    def add_transaction(

            self,

            transaction

    ):

        customer_id = (

            transaction["customer_id"]
        )

        self.customer_history[
            customer_id
        ].append(

            transaction
        )

    def get_history(

            self,

            customer_id

    ):

        return list(

            self.customer_history[
                customer_id
            ]
        )