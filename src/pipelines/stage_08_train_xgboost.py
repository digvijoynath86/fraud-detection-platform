from src.training.xgboost_trainer import (
    XGBoostTrainer
)


def main():

    trainer = XGBoostTrainer()

    trainer.execute()


if __name__ == "__main__":
    main()