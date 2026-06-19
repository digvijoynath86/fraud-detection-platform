import json
from collections import defaultdict
from datetime import datetime

from kafka import KafkaConsumer

from src.utils.config_loader import (
    load_config
)


class AlertService:

    def __init__(self):

        config = load_config()

        kafka_config = config["kafka"]

        self.consumer = KafkaConsumer(

            kafka_config["topics"]["fraud_alerts"],

            bootstrap_servers=(
                kafka_config["bootstrap_servers"]
            ),

            value_deserializer=lambda m:
            json.loads(
                m.decode("utf-8")
            ),

            group_id=(
                kafka_config[
                    "alert_consumer"
                ]["consumer_group"]
            ),

            auto_offset_reset=(
                kafka_config[
                    "alert_consumer"
                ]["auto_offset_reset"]
            )
        )

        self.total_alerts = 0

        self.country_distribution = defaultdict(int)

        self.device_distribution = defaultdict(int)

        self.alert_scores = []

        self.start_time = datetime.now()

    def update_metrics(
            self,
            transaction
    ):

        self.total_alerts += 1

        self.country_distribution[
            transaction["country"]
        ] += 1

        self.device_distribution[
            transaction["device"]
        ] += 1

        self.alert_scores.append(

            transaction["fraud_score"]
        )

    def print_dashboard(self):

        avg_score = round(

            sum(self.alert_scores)

            / len(self.alert_scores),

            3

        ) if self.alert_scores else 0

        print("\n========== FRAUD OPS DASHBOARD ==========")

        print(
            f"Total Alerts: "
            f"{self.total_alerts}"
        )

        print(
            f"Average Fraud Score: "
            f"{avg_score}"
        )

        print(
            f"Top Countries: "
            f"{dict(self.country_distribution)}"
        )

        print(
            f"Devices: "
            f"{dict(self.device_distribution)}"
        )

        print(
            "=========================================\n"
        )

    def run(self):

        print(
            "Alert Service Started..."
        )

        for message in self.consumer:

            transaction = message.value

            self.update_metrics(
                transaction
            )

            print(

                f"ALERT | "

                f"{transaction['transaction_id']} | "

                f"{transaction['customer_id']} | "

                f"Score={transaction['fraud_score']}"
            )

            if self.total_alerts % 10 == 0:

                self.print_dashboard()


def main():

    service = AlertService()

    service.run()


if __name__ == "__main__":

    main()