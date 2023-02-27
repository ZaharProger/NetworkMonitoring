from enum import Enum
from dataclasses import dataclass
from re import compile


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
    NOT_EMPTY_HOST = ValidationCase('[\\S]+', 'Пропущены доменное имя или IP')
    CORRECT_DOMAIN = ValidationCase('^[a-zA-Zа-яА-Я0-9-.]+\\.?[a-zA-Zа-яА-Я]+$',
                                    'Доменное имя содержит недопустимые символы')
    CORRECT_IP = ValidationCase('^(?:(?:25[0-5]|2[0-4][0-9]|1[0-9][0-9]|[1-9][0-9]|[0-9])\\.){3}(?:25[0-5]|2[0-4]['
                                '0-9]|1[0-9][0-9]|[1-9][0-9]|[0-9])$',
                                'IP адрес содержит некорректные символы')


def validate_str(data: str, cases: list[ValidationTypes]) -> dict[ValidationTypes, ValidationResult]:
    results = {}

    for case in cases:
        regex = compile(case.value.regex)
        result = regex.match(data) is not None
        message = case.value.message_if_fails if not result else ''

        results[case] = ValidationResult(result, message)

    return results
