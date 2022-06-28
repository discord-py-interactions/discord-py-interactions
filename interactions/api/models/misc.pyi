import datetime
from enum import IntEnum
from io import FileIO, IOBase
from logging import Logger
from typing import List, Optional, Union

from interactions.api.models.attrs_utils import DictSerializerMixin, define

log: Logger

@define()
class AutoModMetaData(DictSerializerMixin):
    channel_id: Optional[Snowflake]
    duration_seconds: Optional[int]

class AutoModTriggerType(IntEnum):
    KEYWORD: int
    HARMFUL_LINK: int
    SPAM: int
    KEYWORD_PRESET: int

class AutoModKeywordPresetTypes(IntEnum):
    PROFANITY: int
    SEXUAL_CONTENT: int
    SLURS: int

@define()
class AutoModAction(DictSerializerMixin):
    type: int
    metadata: Optional[AutoModMetaData]

@define()
class AutoModTriggerMetadata(DictSerializerMixin):
    keyword_filter: Optional[List[str]]
    presets: Optional[List[str]]

@define()
class Overwrite(DictSerializerMixin):
    id: int
    type: int
    allow: str
    deny: str

@define()
class ClientStatus(DictSerializerMixin):
    desktop: Optional[str]
    mobile: Optional[str]
    web: Optional[str]

class Snowflake:
    _snowflake: str
    def __init__(self, snowflake: Union[int, str, "Snowflake"]) -> None: ...
    def __int__(self): ...
    @property
    def increment(self) -> int: ...
    @property
    def worker_id(self) -> int: ...

    @property
    def process_id(self) -> int: ...

    @property
    def epoch(self) -> float: ...

    @property
    def timestamp(self) -> datetime.datetime: ...

    def __hash__(self): ...

    def __eq__(self, other): ...


class IDMixin:
    """A mixin to implement equality and hashing for models that have an id."""
    id: Snowflake

    def __eq__(self, other): ...

    def __hash__(self): ...


class Color:
    @staticmethod
    def blurple() -> hex: ...
    @staticmethod
    def green() -> hex: ...
    @staticmethod
    def yellow() -> hex: ...
    @staticmethod
    def fuchsia() -> hex: ...
    @staticmethod
    def red() -> hex: ...
    @staticmethod
    def white() -> hex: ...
    @staticmethod
    def black() -> hex: ...


class File:
    def __init__(
        self, filename: str, fp: Optional[IOBase] = ..., description: Optional[str] = ...
    ) -> None: ...

class Image:
    _URI: str
    _name: str

    def __init__(self, file: Union[str, FileIO], fp: Optional[IOBase] = ...) -> None: ...
    @property
    def data(self) -> str: ...
    @property
    def filename(self) -> str: ...
