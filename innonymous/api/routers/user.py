from base64 import b64encode
from uuid import UUID, uuid4

from fastapi import APIRouter, Depends, HTTPException, status

from innonymous.api.dependencies import get_captcha_service, get_jwt_service
from innonymous.api.models import (
    ConfirmUserRegistrationForm,
    UnconfirmedUserTokenPayload,
    User,
    UserInfo,
    UserLogInForm,
    UserRegistrationForm,
    UserRegistrationResponse,
    UserSession,
)
from innonymous.api.use_case.user import CreateUserSessionUseCase
from innonymous.repository import AnyRepository, UserRepository
from innonymous.security import Captcha, CaptchaService, JwtService, Password

user_router = APIRouter(tags=["users"])


@user_router.get("/user/view/{uuid}", response_model=UserInfo)
async def get_by_uuid(uuid: UUID, users: AnyRepository[User, str] = Depends(UserRepository.create)) -> UserInfo:
    user = await users.get(str(uuid))
    if user is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="No user with such UUID")

    return UserInfo(name=user.name, uuid=user.uuid)


@user_router.post("/user/new", response_model=UserRegistrationResponse)
async def register_new(
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


@user_router.post("/user/new/confirm", response_model=UserSession)
async def confirm_registration(
        confirm_form: ConfirmUserRegistrationForm,
        users: AnyRepository[User, str] = Depends(UserRepository.create),
        captcha_service: CaptchaService = Depends(get_captcha_service),
        jwt_service: JwtService = Depends(get_jwt_service),
) -> UserSession:
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

    user = await users.save(
        User(
            name=unconfirmed_user_data.name,
            uuid=str(uuid4()),
            password=Password.encrypt(confirm_form.password),
            token_expires_at=jwt_service.expiration_time.from_now(),
        )
    )

    return await CreateUserSessionUseCase(user.name, users, jwt_service).execute()


@user_router.post("/user/login", response_model=UserSession)
async def log_in(
        login_form: UserLogInForm,
        users: AnyRepository[User, str] = Depends(UserRepository.create),
        jwt_service: JwtService = Depends(get_jwt_service),
) -> UserSession:
    user = await users.get(login_form.name)
    if user is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"User `{login_form.name}` not found")

    if not Password.is_valid(login_form.password, user.password):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Wrong password")

    return await CreateUserSessionUseCase(user.name, users, jwt_service).execute()
