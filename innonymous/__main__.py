from fastapi import FastAPI

from innonymous.api.routers import user_router
from innonymous.mongo_collections import MongoCollections

app = FastAPI(title="Innonymous", root_path="")


@app.on_event("startup")
async def on_startup() -> None:
    await MongoCollections.bind_to_database()


@app.get("/")
async def root() -> str:
    return "greg"


app.include_router(user_router)
