import json

import redis


class RedisHistoryStore:

    def __init__(

            self,

            host="localhost",

            port=6379,

            history_size=50

    ):

        self.redis_client = redis.Redis(

            host=host,

            port=port,

            decode_responses=True
        )

        self.history_size = history_size

    def get_key(

            self,

            customer_id

    ):

        return f"customer:{customer_id}"

    def add_transaction(

            self,

            transaction

    ):

        customer_id = (

            transaction["customer_id"]
        )

        key = self.get_key(

            customer_id
        )

        self.redis_client.lpush(

            key,

            json.dumps(
                transaction
            )
        )

        self.redis_client.ltrim(

            key,

            0,

            self.history_size - 1
        )

    def get_history(

            self,

            customer_id

    ):

        key = self.get_key(

            customer_id
        )

        history = self.redis_client.lrange(

            key,

            0,

            -1
        )

        return [

            json.loads(txn)

            for txn in history
        ]