from fastapi import FastAPI

from innonymous.mongo_storage import MongoStorage

app = FastAPI(title="Innonymous", root_path="")


@app.on_event("startup")
async def on_startup() -> None:
    await MongoStorage.bind_to_database()


@app.get("/")
async def root() -> str:
    return "greg"
