from src.feature_engineering.business_feature_builder import (
    BusinessFeatureBuilder
)


def main():

    builder = (
        BusinessFeatureBuilder()
    )

    builder.execute()


if __name__ == "__main__":
    main()