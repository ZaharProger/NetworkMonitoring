from dataclasses import dataclass


@dataclass
class Port:
    value: int
    is_opened: bool


@dataclass
class Host:
    domain_name: str
    ip_addresses: list[str]
    ports: list[Port]
