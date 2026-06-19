from src.services.transaction_service.customer_profile_generator import (
    CustomerProfileGenerator
)

from src.services.transaction_service.transaction_generator import (
    TransactionGenerator
)


def main():

    profile_generator = (

        CustomerProfileGenerator()

    )

    profiles = (

        profile_generator.generate_profiles(

            n_customers=5
        )
    )

    transaction_generator = (

        TransactionGenerator()

    )

    for customer_id, profile in profiles.items():

        transaction = (

            transaction_generator.generate_transaction(

                customer_id,

                profile
            )
        )

        print(transaction)

        print()


if __name__ == "__main__":

    main()