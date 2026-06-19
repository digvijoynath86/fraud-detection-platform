import random


class CustomerProfileGenerator:

    def __init__(self):

        self.merchants = [

            "AMAZON",
            "APPLE",
            "UBER",
            "NETFLIX",
            "FLIPKART",
            "SWIGGY",
            "ZOMATO",
            "WALMART"
        ]

        self.devices = [

            "mobile",

            "desktop",

            "tablet"
        ]

        self.countries = [

            "IN",

            "US",

            "UK",

            "SG",

            "AU"
        ]

        self.email_domains = [

            "gmail.com",

            "yahoo.com",

            "hotmail.com",

            "outlook.com"
        ]

    def generate_profiles(
            self,
            n_customers=100
    ):

        profiles = {}

        for i in range(
                1,
                n_customers + 1
        ):

            customer_id = (
                f"CUST{i:06d}"
            )

            avg_spend = random.randint(
                500,
                10000
            )

            profiles[
                customer_id
            ] = {

                "home_country":

                    random.choice(
                        self.countries
                    ),

                "avg_spend":

                    avg_spend,

                "spend_std":

                    int(
                        avg_spend * 0.3
                    ),

                "preferred_merchants":

                    random.sample(
                        self.merchants,
                        k=3
                    ),

                "preferred_device":

                    random.choice(
                        self.devices
                    ),

                "email_domain":

                    random.choice(
                        self.email_domains
                    ),
                "risk_mode": False,

                "risk_countdown": 0,

                "fraud_scenario": None
            }

        return profiles