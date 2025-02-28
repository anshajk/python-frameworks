import asyncio
from fastapi import FastAPI

app = FastAPI()


@app.get("/sync")
def sync_endpoint():
    import time

    time.sleep(2)  # Blocking operation
    return {"message": "This response was delayed by 2 seconds (sync)"}


@app.get("/async")
async def async_endpoint():
    await asyncio.sleep(2)  # Non-blocking operation
    return {"message": "This response was delayed by 2 seconds (async)"}
