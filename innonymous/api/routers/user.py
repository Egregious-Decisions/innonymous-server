from uuid import UUID, uuid4
from bson.binary import UUID

from fastapi import APIRouter

from innonymous.api.models import User, UserCreateSchema
from innonymous.repository import UserRepository

user_router = APIRouter(tags=["users"])


@user_router.get("/user/{uuid}", response_model=User)
async def get_by_uuid(uuid: UUID) -> User:
    users = UserRepository.create()
    user = await users.get(str(uuid))
    if user is None:
        raise
    return user


@user_router.post("/user/new", response_model=User)
async def create_new(user: UserCreateSchema) -> User:
    new_user = User(uuid=str(uuid4()), name=user.name)
    users = UserRepository.create()
    return await users.save(new_user)
