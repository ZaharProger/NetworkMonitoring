from dataclasses import dataclass
from enum import Enum


@dataclass
class ValidationCase:
    regex: str
    message_if_fails: str


@dataclass
class ValidationResult:
    result: bool
    message: str


class ValidationTypes(Enum):
    CORRECT_PORT = ValidationCase('[0-9]+', 'Порт содержит некорректные символы')
    NOT_EMPTY_HOST = ValidationCase('[\\S]+', 'Пропущено доменное имя или IP')
    CORRECT_DOMAIN = ValidationCase('^[a-zA-Zа-яА-Я0-9-.]+\\.?[a-zA-Zа-яА-Я]+$',
                                    'Доменное имя содержит недопустимые символы')
    CORRECT_IP = ValidationCase('^(?:(?:25[0-5]|2[0-4][0-9]|1[0-9][0-9]|[1-9][0-9]|[0-9])\\.){3}(?:25[0-5]|2[0-4]['
                                '0-9]|1[0-9][0-9]|[1-9][0-9]|[0-9])$',
                                'IP адрес содержит некорректные символы')


@dataclass
class Host:
    domain_name: str
    ip_addresses: list[str]
    ports: list[int]
