from innonymous.security import CaptchaService, JwtService
from innonymous.settings import Settings

jwt_service = JwtService(key=Settings.api.key, ttl_seconds=Settings.api.jwt_ttl_seconds)
captcha_service = CaptchaService(key=Settings.api.key, ttl_seconds=Settings.api.captcha_ttl_seconds)


def get_jwt_service() -> JwtService:
    return jwt_service


def get_captcha_service() -> CaptchaService:
    return captcha_service
