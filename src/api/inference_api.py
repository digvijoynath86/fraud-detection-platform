from fastapi import FastAPI

from models.tab_transformer.predictor import (
    TabTransformerPredictor
)

app = FastAPI()

predictor = (

    TabTransformerPredictor()

)


@app.get("/health")

def health():

    return {

        "status": "healthy"
    }


@app.post("/predict")

def predict(

        payload: dict

):

    history = payload["history"]

    score = (

        predictor.predict(

            history
        )
    )

    return {

        "fraud_score": score
    }

from src.feature_store.redis_history_store import (
    RedisHistoryStore
)

redis_store = RedisHistoryStore()


@app.get("/test_customer")

def test_customer():

    keys = redis_store.redis_client.keys(
        "customer:*"
    )

    if not keys:

        return {
            "error": "Redis empty"
        }

    customer_key = keys[0]

    customer_id = customer_key.replace(
        "customer:",
        ""
    )

    history = redis_store.get_history(
        customer_id
    )

    score = predictor.predict(
        history
    )

    return {

        "customer_id": customer_id,

        "history_size": len(history),

        "fraud_score": score
    }