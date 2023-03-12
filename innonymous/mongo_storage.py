from motor.motor_asyncio import AsyncIOMotorClient  # type: ignore
from pymotyc import Engine as PymotycEngine, Collection  # type: ignore

from innonymous.settings import Settings

pymotyc_engine = PymotycEngine()


@pymotyc_engine.database
class MongoStorage:
    # users: Collection[User] = Collection(identity="id")

    @classmethod
    async def bind_to_database(cls):
        motor = AsyncIOMotorClient(Settings.mongo.url)
        await pymotyc_engine.bind(motor=motor, inject_motyc_fields=True)
