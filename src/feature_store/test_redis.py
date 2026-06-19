from src.feature_store.redis_history_store import (
    RedisHistoryStore
)


def main():

    store = RedisHistoryStore()

    keys = store.redis_client.keys(
        "customer:*"
    )

    print(

        f"Customers in Redis: "

        f"{len(keys)}"

    )

    print()

    print(

        "Sample customers:"

    )

    for key in keys[:5]:

        history = (

            store.redis_client.llen(
                key
            )
        )

        print(

            key,

            history
        )


if __name__ == "__main__":

    main()