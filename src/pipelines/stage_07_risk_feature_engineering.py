from src.feature_engineering.risk_feature_builder import (
    RiskFeatureBuilder
)


def main():

    builder = (
        RiskFeatureBuilder()
    )

    builder.execute()


if __name__ == "__main__":
    main()