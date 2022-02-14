from dataclasses import dataclass
from enum import Enum


class ArgsType(Enum):
    Date = 1
    Name = 2


@dataclass
class Arg:
    type: ArgsType
    required: bool


@dataclass
class Group:
    keywords: list[str]


@dataclass
class BaseCommand:
    command: str
    groups: list[Group]
    # hasArg: bool
    args: list[Arg]