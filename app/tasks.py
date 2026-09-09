import os
import redis

REDIS_URL = os.getenv("REDIS_URL", "redis://localhost:6379/0")

def enqueue_shopping_task(task_name: str, payload: str):
    client = redis.from_url(REDIS_URL)
    client.rpush(
        "buywise:tasks",
        f"{task_name}:{payload}"
    )
    return {"queued": True, "task": task_name}
