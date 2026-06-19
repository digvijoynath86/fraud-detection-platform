import json
import random
import time

from kafka import KafkaProducer

from src.services.transaction_service.customer_profile_generator import (
    CustomerProfileGenerator
)

from src.services.transaction_service.transaction_generator import (
    TransactionGenerator
)

from src.utils.config_loader import (
    load_config
)

class TransactionProducer:

    def __init__(self):

        config = load_config()

        self.kafka_config = config["kafka"]

        self.topic = (

            self.kafka_config

            ["topics"]

            ["transactions"]
        )



        self.producer = KafkaProducer(

            bootstrap_servers=(

                self.kafka_config

                ["bootstrap_servers"]
            )
            ,

            value_serializer=lambda v:

            json.dumps(v).encode("utf-8")
        )

        self.profile_generator = (
            CustomerProfileGenerator()
        )

        self.transaction_generator = (
            TransactionGenerator()
        )

        self.customer_profiles = (
            self.profile_generator.generate_profiles(
                n_customers=(

                    self.kafka_config

                    ["producer"]

                    ["customer_pool_size"]
                )
            )
        )
        self.total_transactions = 0
        self.total_frauds = 0

    def publish_transaction(self):

        customer_id = random.choice(

            list(
                self.customer_profiles.keys()
            )
        )

        profile = self.customer_profiles[
            customer_id
        ]

        transaction = (

            self.transaction_generator.generate_transaction(

                customer_id,

                profile
            )
        )

        self.producer.send(

            self.topic,

            value=transaction
        )

        self.producer.flush()

        self.total_transactions += 1

        if transaction["is_fraud"]:
            self.total_frauds += 1

        return transaction

    def run(
            self,
            transactions_per_second=10
    ):

        sleep_time = (
                1 / transactions_per_second
        )

        print(
            f"Producer started at "
            f"{transactions_per_second} TPS"
        )

        counter = 0

        while True:

            transaction = (
                self.publish_transaction()
            )

            counter += 1

            if counter % 100 == 0:
                print(

                    f"Transactions: "

                    f"{self.total_transactions} | "

                    f"Frauds: "

                    f"{self.total_frauds}"
                )

            time.sleep(
                sleep_time
            )


def main():

    producer = (
        TransactionProducer()
    )

    producer.run(
        transactions_per_second=(

            producer.kafka_config

            ["producer"]

            ["transactions_per_second"]
        )
    )


if __name__ == "__main__":

    main()