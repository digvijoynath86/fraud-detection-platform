from models.tab_transformer.dataset_builder import (
    DatasetBuilder
)


def main():

    builder = DatasetBuilder(

        n_customers=1000,

        transactions_per_customer=100

    )

    builder.execute()


if __name__ == "__main__":

    main()