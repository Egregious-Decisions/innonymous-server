from datetime import datetime, timedelta, timezone


class ExpirationTime:
    def __init__(self, seconds: int) -> None:
        if seconds < 0:
            error_msg = "Cannot have negative expiration time"
            raise ValueError(error_msg)

        self.__seconds = seconds

    @property
    def seconds(self) -> int:
        return self.__seconds

    def from_point(self, time: datetime) -> datetime:
        return time + timedelta(seconds=self.__seconds)

    def from_now(self) -> datetime:
        return self.from_point(self.__time_now())

    @classmethod
    def is_in_future(cls, expiration_time: datetime) -> bool:
        return cls.__time_now() < expiration_time

    @classmethod
    def __time_now(cls) -> datetime:
        return datetime.now(tz=timezone.utc)
