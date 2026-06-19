from src.mlflow.mlflow_tracker import (
    MLflowTracker
)


def main():

    tracker = (
        MLflowTracker()
    )

    tracker.execute()


if __name__ == "__main__":
    main()