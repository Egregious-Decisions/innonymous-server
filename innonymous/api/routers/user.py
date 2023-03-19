from uuid import UUID, uuid4

from fastapi import APIRouter, Depends

from innonymous.api.models import User, UserCreateSchema
from innonymous.repository import AnyRepository, UserRepository

user_router = APIRouter(tags=["users"])


@user_router.get("/user/{uuid}", response_model=User)
async def get_by_uuid(uuid: UUID, users: AnyRepository[User, str] = Depends(UserRepository.create)) -> User:
    user = await users.get(str(uuid))
    if user is None:
        raise
    return user


@user_router.post("/user/new", response_model=User)
async def create_new(user: UserCreateSchema, users: AnyRepository[User, str] = Depends(UserRepository.create)) -> User:
    new_user = User(uuid=str(uuid4()), name=user.name)
    return await users.save(new_user)
