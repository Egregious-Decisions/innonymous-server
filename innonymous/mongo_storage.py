from motor.motor_asyncio import AsyncIOMotorClient
from pymotyc import Engine as PymotycEngine

from innonymous.settings import Settings

pymotyc_engine = PymotycEngine()


@pymotyc_engine.database
class MongoStorage:
    @classmethod
    async def bind_to_database(cls) -> None:
        motor = AsyncIOMotorClient(Settings.mongo.url)
        await pymotyc_engine.bind(motor=motor, inject_motyc_fields=True)
