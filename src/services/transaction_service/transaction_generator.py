import random

from datetime import datetime, timezone


class TransactionGenerator:

    def __init__(self):

        self.fraud_probability = 0.03

        self.high_risk_countries = [

            "RU",
            "NG",
            "KP"
        ]

        self.all_merchants = [

            "AMAZON",
            "APPLE",
            "UBER",
            "NETFLIX",
            "FLIPKART",
            "SWIGGY",
            "ZOMATO",
            "WALMART",
            "UNKNOWN_MERCHANT"
        ]

        self.all_devices = [

            "mobile",

            "desktop",

            "tablet"
        ]

    def generate_transaction(

            self,

            customer_id,

            profile

    ):

        if (

                not profile["risk_mode"]

                and

                random.random() < 0.02

        ):
            self.trigger_risk_journey(

                profile
            )

        if profile["risk_mode"]:
            return self.generate_risk_transaction(

                customer_id,

                profile
            )

        return self.generate_normal_transaction(

            customer_id,

            profile
        )

    def generate_normal_transaction(
            self,
            customer_id,
            profile
    ):

        amount = max(

            50,

            round(

                random.gauss(

                    profile["avg_spend"],

                    profile["spend_std"]
                ),

                2
            )
        )

        transaction = {

            "transaction_id":

                f"TX{random.randint(100000000,999999999)}",

            "customer_id":

                customer_id,

            "amount":

                amount,

            "merchant":

                random.choice(

                    profile[
                        "preferred_merchants"
                    ]
                ),

            "device":

                profile[
                    "preferred_device"
                ],

            "country":

                profile[
                    "home_country"
                ],

            "email_domain":

                profile[
                    "email_domain"
                ],

            "is_fraud":

                0,

            "timestamp":

                datetime.now(

                    timezone.utc

                ).isoformat()
        }

        return transaction

    def generate_fraud_transaction(
            self,
            customer_id,
            profile
    ):

        amount = round(

            profile["avg_spend"]

            * random.uniform(

                5,

                20
            ),

            2
        )

        transaction = {

            "transaction_id":

                f"TX{random.randint(100000000,999999999)}",

            "customer_id":

                customer_id,

            "amount":

                amount,

            "merchant":

                "UNKNOWN_MERCHANT",

            "device":

                random.choice(

                    self.all_devices
                ),

            "country":

                random.choice(

                    self.high_risk_countries
                ),

            "email_domain":

                profile[
                    "email_domain"
                ],

            "is_fraud":

                1,

            "timestamp":

                datetime.now(

                    timezone.utc

                ).isoformat()
        }

        return transaction

    def trigger_risk_journey(
            self,
            profile
    ):
        scenarios = [

            "account_takeover",

            "merchant_escalation",

            "amount_escalation",

            "velocity_attack"
        ]

        profile["risk_mode"] = True

        profile["risk_countdown"] = 5

        profile["fraud_scenario"] = (

            random.choices(

                scenarios,

                weights=[40, 30, 20, 10]

            )[0]
        )

    def generate_risk_transaction(

            self,

            customer_id,

            profile

    ):

        scenario = (

            profile["fraud_scenario"]
        )

        countdown = (

            profile["risk_countdown"]
        )

        is_fraud = (

                countdown == 1
        )

        amount = profile["avg_spend"]

        merchant = random.choice(

            profile["preferred_merchants"]
        )

        country = profile["home_country"]

        device = profile["preferred_device"]

        if scenario == "account_takeover":

            amount *= random.uniform(

                5,

                20
            )

            merchant = "UNKNOWN"

            country = "RU"

            device = "desktop"

        elif scenario == "merchant_escalation":

            amount *= random.uniform(

                2,

                10
            )

            merchant = "UNKNOWN"

        elif scenario == "amount_escalation":

            amount *= (

                    6 - countdown
            )

        elif scenario == "velocity_attack":

            amount *= random.uniform(

                3,

                8
            )

        profile["risk_countdown"] -= 1

        if (

                profile["risk_countdown"]

                == 0
        ):
            profile["risk_mode"] = False

            profile["fraud_scenario"] = None

        return {

            "transaction_id":

                f"TX{random.randint(100000000, 999999999)}",

            "customer_id":

                customer_id,

            "amount":

                round(

                    amount,

                    2
                ),

            "merchant":

                merchant,

            "device":

                device,

            "country":

                country,

            "email_domain":

                profile["email_domain"],

            "is_fraud":

                int(is_fraud),

            "timestamp":

                datetime.now(

                    timezone.utc

                ).isoformat()
        }