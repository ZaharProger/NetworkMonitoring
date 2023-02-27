from dataclasses import dataclass
from enum import Enum


class HostTypes(Enum):
    DOMAIN = 0
    IP = 1


@dataclass
class Port:
    name: str
    is_opened: bool


@dataclass
class Host:
    host_type: HostTypes
    name: str
    ports: list[Port]
