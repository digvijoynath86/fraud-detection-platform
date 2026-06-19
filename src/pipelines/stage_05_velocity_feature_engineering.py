from src.feature_engineering.velocity_feature_builder import (
    VelocityFeatureBuilder
)


def main():

    builder = VelocityFeatureBuilder()

    builder.execute()


if __name__ == "__main__":
    main()