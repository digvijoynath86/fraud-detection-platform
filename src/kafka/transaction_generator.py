import random

from datetime import datetime, timezone


class TransactionGenerator:

    def __init__(self):

        self.customers = [

            f"CUST{i:05d}"

            for i in range(
                1,
                1001
            )
        ]

        self.merchants = [

            "AMAZON",
            "UBER",
            "NETFLIX",
            "APPLE",
            "FLIPKART",
            "SWIGGY",
            "ZOMATO",
            "WALMART"

        ]

        self.payment_methods = [

            "credit",

            "debit"
        ]

        self.device_types = [

            "mobile",

            "desktop",

            "tablet"
        ]

        self.email_domains = [

            "gmail.com",

            "yahoo.com",

            "hotmail.com"
        ]

        self.countries = [

            "IN",

            "US",

            "UK"
        ]

    def generate_transaction(self):

        customer = random.choice(
            self.customers
        )

        transaction = {

            "transaction_id":

                f"TX{random.randint(100000,999999)}",

            "customer_id":

                customer,

            "amount":

                round(
                    random.uniform(
                        100,
                        5000
                    ),
                    2
                ),

            "merchant_id":

                random.choice(
                    self.merchants
                ),

            "payment_method":

                random.choice(
                    self.payment_methods
                ),

            "device_type":

                random.choice(
                    self.device_types
                ),

            "email_domain":

                random.choice(
                    self.email_domains
                ),

            "country":

                random.choice(
                    self.countries
                ),

            "timestamp":

                datetime.now(
                    timezone.utc
                ).isoformat()
        }

        return transaction