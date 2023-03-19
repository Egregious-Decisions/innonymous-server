from motor.motor_asyncio import AsyncIOMotorClient
from pymotyc import Collection, Engine as PymotycEngine

from innonymous.api.models import ChatRoom, Message, User
from innonymous.settings import Settings

pymotyc_engine = PymotycEngine()


@pymotyc_engine.database
class MongoCollections:
    chat_rooms: Collection[ChatRoom] = Collection()
    messages: Collection[Message] = Collection()
    users: Collection[User] = Collection()

    @classmethod
    async def bind_to_database(cls) -> None:
        motor = AsyncIOMotorClient(Settings.mongo.url)
        await pymotyc_engine.bind(motor=motor, inject_motyc_fields=True)
