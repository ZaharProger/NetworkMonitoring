from re import compile

from .entities import ValidationTypes, ValidationResult


def validate_str(data: str, cases: list[ValidationTypes]) -> dict[ValidationTypes, ValidationResult]:
    results = {}

    for case in cases:
        regex = compile(case.value.regex)
        result = regex.match(data) is not None
        message = case.value.message_if_fails if not result else ''

        results[case] = ValidationResult(result, message)

    return results
