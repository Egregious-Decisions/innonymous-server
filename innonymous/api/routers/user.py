from base64 import b64encode
from uuid import UUID

import bcrypt
from fastapi import APIRouter, Depends, HTTPException, status

from innonymous.api.dependencies import get_captcha_service, get_jwt_service
from innonymous.api.models import (
    ConfirmUserRegistrationForm,
    UnconfirmedUserTokenPayload,
    User,
    UserAccess,
    UserAccessTokenPayload,
    UserRegistrationForm,
    UserRegistrationResponse,
)
from innonymous.repository import AnyRepository, UserRepository
from innonymous.security import Captcha, CaptchaService, JwtService

user_router = APIRouter(tags=["users"])


@user_router.get("/user/{uuid}", response_model=User)
async def get_by_uuid(uuid: UUID, users: AnyRepository[User, str] = Depends(UserRepository.create)) -> User:
    user = await users.get(str(uuid))
    if user is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="No user with such UUID")

    return user


@user_router.post("/user/new", response_model=UserRegistrationResponse)
async def create(
    user_form: UserRegistrationForm,
    users: AnyRepository[User, str] = Depends(UserRepository.create),
    captcha_service: CaptchaService = Depends(get_captcha_service),
    jwt_service: JwtService = Depends(get_jwt_service),
) -> UserRegistrationResponse:
    if await users.exists(user_form.name):
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Nickname already taken")

    captcha = captcha_service.generate()

    unconfirmed_user_data = UnconfirmedUserTokenPayload(
        name=user_form.name, captcha_passphrase=captcha.hashed_passphrase, captcha_expires_at=captcha.expires_at
    )

    return UserRegistrationResponse(
        pre_registration_token=jwt_service.encode(unconfirmed_user_data),
        captcha_image=b64encode(captcha.image).decode(),
    )


@user_router.post("/users/new/confirm", response_model=UserAccess)
async def confirm(
    confirm_form: ConfirmUserRegistrationForm,
    users: AnyRepository[User, str] = Depends(UserRepository.create),
    captcha_service: CaptchaService = Depends(get_captcha_service),
    jwt_service: JwtService = Depends(get_jwt_service),
) -> UserAccess:
    try:
        unconfirmed_user_data = jwt_service.decode(confirm_form.pre_registration_token, UnconfirmedUserTokenPayload)
    except Exception as ex:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Invalid token") from ex

    if await users.exists(unconfirmed_user_data.name):
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Nickname already exists")

    original_captcha = Captcha(
        hashed_passphrase=unconfirmed_user_data.captcha_passphrase,
        expires_at=unconfirmed_user_data.captcha_expires_at,
        image=b"",
    )

    if not captcha_service.is_valid(confirm_form.captcha_user_input, original_captcha):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Invalid Captcha")

    if captcha_service.is_expired(original_captcha):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Token expired")

    salt = bcrypt.gensalt()
    hashed_password = bcrypt.hashpw(confirm_form.password.encode("utf-8"), salt)

    user = await users.save(
        User(
            name=unconfirmed_user_data.name,
            password=hashed_password,
            salt=salt,
            token_expires_at=jwt_service.expiration_time.from_now(),
        )
    )

    access_token_payload = UserAccessTokenPayload(name=user.name, expires_at=user.token_expires_at)

    return UserAccess(name=user.name, token=jwt_service.encode(access_token_payload))
