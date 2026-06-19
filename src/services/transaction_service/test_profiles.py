from src.services.transaction_service.customer_profile_generator import (
    CustomerProfileGenerator
)


def main():

    generator = (
        CustomerProfileGenerator()
    )

    profiles = (
        generator.generate_profiles(
            n_customers=5
        )
    )

    for k, v in profiles.items():

        print(k)

        print(v)

        print()


if __name__ == "__main__":

    main()