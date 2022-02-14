from dataclasses import dataclass
from enum import Enum


class ArgsType(Enum):
    Date = "date"
    Name = "name"


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
