from innonymous.api.models.user import User, UserAccessTokenPayload, UserSession
from innonymous.repository.any_repository import AnyRepository
from innonymous.security import JwtService


class CreateUserSessionUseCase:
    def __init__(self, user_name: str, users: AnyRepository[User, str], jwt_service: JwtService) -> None:
        self.user_name = user_name
        self.users = users
        self.jwt_service = jwt_service

    async def execute(self) -> UserSession:
        user = await self.users.get(self.user_name)
        if user is None:
            msg = "The user must already be created"
            raise RuntimeError(msg)

        user.token_expires_at = self.jwt_service.expiration_time.from_now()
        user = await self.users.save(user)

        access_token_payload = UserAccessTokenPayload(name=user.name, expires_at=user.token_expires_at)
        return UserSession(uuid=user.uuid, token=self.jwt_service.encode(access_token_payload))
