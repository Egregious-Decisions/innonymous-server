from innonymous.security import CaptchaService, JwtService
from innonymous.settings import Settings


def get_jwt_service() -> JwtService:
    return JwtService(key=Settings.api.key, ttl_seconds=Settings.api.jwt_ttl_seconds)


def get_captcha_service() -> CaptchaService:
    return CaptchaService(key=Settings.api.key, ttl_seconds=Settings.api.captcha_ttl_seconds)
