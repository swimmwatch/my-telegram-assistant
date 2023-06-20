import random

from fastapi import FastAPI

app = FastAPI()


@app.get("/api/test")
async def reply_square():
    return {"num": random.randint(1, 10) ** 2}
