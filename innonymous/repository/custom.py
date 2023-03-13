from innonymous.api.models import User
from innonymous.mongo_collections import MongoCollections
from innonymous.repository.mongo_repository import make_mongo_repository_type

UserRepository = make_mongo_repository_type(
    mongo_model=User, collection=MongoCollections.users, id_reference=lambda: User.uuid
)
