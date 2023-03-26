import hmac
import string
from dataclasses import dataclass
from datetime import datetime
from random import SystemRandom

from captcha.image import ImageCaptcha  # type: ignore # noqa: PGH003

from innonymous.security.expiration_time import ExpirationTime


@dataclass(frozen=True)
class Captcha:
    hashed_passphrase: str
    image: bytes
    expires_at: datetime


class CaptchaService:
    algorithm = "SHA256"

    def __init__(self, key: str, ttl_seconds: int, *, length: int = 4) -> None:
        self.__key = key.encode()
        self.__length = length
        self.__image_captcha: ImageCaptcha = ImageCaptcha()
        self.__expiration_time = ExpirationTime(ttl_seconds)

    @property
    def expiration_time(self) -> ExpirationTime:
        return self.__expiration_time

    @classmethod
    def alphabet(cls) -> str:
        hard_to_distinguish = set("9q 0o cda 17 uv 6b")
        full_alphabet = set(string.digits + string.ascii_lowercase)
        return "".join(full_alphabet.difference(hard_to_distinguish))

    def generate(self) -> Captcha:
        passphrase = self.__make_random_passphrase()
        import logging
        logging.critical(passphrase)
        return Captcha(
            hashed_passphrase=self.__encode(passphrase),
            image=self.__make_image(passphrase),
            expires_at=self.expiration_time.from_now(),
        )

    def is_valid(self, given_passphrase: str, original_captcha: Captcha) -> bool:
        return self.__encode(given_passphrase) == original_captcha.hashed_passphrase

    @classmethod
    def is_expired(cls, original_captcha: Captcha) -> bool:
        return not ExpirationTime.is_in_future(original_captcha.expires_at)

    def __make_random_passphrase(self) -> str:
        random_device = SystemRandom()
        return "".join(random_device.choices(self.alphabet(), k=self.__length))

    def __make_image(self, passphrase: str) -> bytes:
        with self.__image_captcha.generate(passphrase, "jpeg") as image_buffer:
            return image_buffer.getvalue()

    def __encode(self, passphrase: str) -> str:
        return hmac.digest(self.__key, passphrase.lower().replace(" ", "").encode(), self.algorithm).hex()
