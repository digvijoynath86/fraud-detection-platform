from src.feature_store.redis_history_store import (
    RedisHistoryStore
)

store = RedisHistoryStore()

keys = store.redis_client.keys("customer:*")

print(f"Total customers = {len(keys)}")

sizes = []

for key in keys:

    sizes.append(
        store.redis_client.llen(key)
    )

print(f"Max history = {max(sizes)}")

print(f"Average history = {sum(sizes)/len(sizes):.2f}")