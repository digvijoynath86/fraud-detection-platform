import json

from kafka import KafkaConsumer
from kafka import KafkaProducer

from src.feature_store.redis_history_store import (
    RedisHistoryStore
)

from src.services.fraud_scoring_service.realtime_feature_builder import (
    RealtimeFeatureBuilder
)

from src.services.fraud_scoring_service.rule_based_scorer import (
    RuleBasedScorer
)

from src.utils.config_loader import (
    load_config
)


class FraudScoringService:

    def __init__(self):

        config = load_config()

        kafka_config = config["kafka"]

        self.transaction_topic = (

            kafka_config["topics"]

            ["transactions"]
        )

        self.alert_topic = (

            kafka_config["topics"]

            ["fraud_alerts"]
        )

        self.consumer = KafkaConsumer(

            self.transaction_topic,

            bootstrap_servers=(

                kafka_config[
                    "bootstrap_servers"
                ]
            ),

            value_deserializer=lambda m:

            json.loads(

                m.decode("utf-8")
            ),

            group_id=(

                kafka_config

                ["consumer"]

                ["consumer_group"]
            ),

            auto_offset_reset=(

                kafka_config

                ["consumer"]

                ["auto_offset_reset"]
            )
        )

        self.producer = KafkaProducer(

            bootstrap_servers=(

                kafka_config[
                    "bootstrap_servers"
                ]
            ),

            value_serializer=lambda v:

            json.dumps(v).encode(
                "utf-8"
            )
        )

        self.history_store = (
            RedisHistoryStore()
        )

        self.feature_builder = (
            RealtimeFeatureBuilder()
        )

        from models.tab_transformer.predictor import (
            TabTransformerPredictor
        )

        self.scorer = (

            TabTransformerPredictor()

        )
        self.rule_engine = (
            RuleBasedScorer()
        )

        self.tab_transformer = (
            TabTransformerPredictor()
        )

    def process_transaction(
            self,
            transaction
    ):

        customer_id = transaction["customer_id"]

        history = self.history_store.get_history(
            customer_id
        )

        sequence = history + [transaction]

        sequence = sequence[-20:]

        if len(history) < 20:

            features = self.feature_builder.build(

                transaction,

                history

            )

            fraud_score = (

                self.rule_engine.score(

                    features

                )
            )

        else:

            fraud_score = (

                self.tab_transformer.predict(

                    sequence

                )
            )

        transaction["fraud_score"] = round(

            fraud_score,

            4
        )

        self.history_store.add_transaction(

            transaction

        )

        return transaction

    def publish_alert(
            self,
            transaction
    ):

        self.producer.send(

            self.alert_topic,

            value=transaction
        )

    def run(self):

        print(
            "Fraud Scoring Service Started..."
        )

        for message in self.consumer:

            transaction = (

                message.value
            )

            scored_transaction = (

                self.process_transaction(
                    transaction
                )
            )

            if (

                scored_transaction[
                    "fraud_score"
                ]

                >= 0.7

            ):

                self.publish_alert(

                    scored_transaction
                )

                print(

                    "ALERT:",

                    scored_transaction[
                        "transaction_id"
                    ],

                    scored_transaction[
                        "fraud_score"
                    ]
                )


def main():

    service = (
        FraudScoringService()
    )

    service.run()


if __name__ == "__main__":

    main()