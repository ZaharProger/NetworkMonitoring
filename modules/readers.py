import csv
import json
from abc import ABC, abstractmethod
from contextlib import closing

from .entities import Host, Port
from .validation import ValidationTypes, validate_str


class Reader(ABC):
    def __init__(self, path: str):
        self.path = path

    @abstractmethod
    def get_data(self) -> list[Host]:
        ...


class CsvReader(Reader):
    def __init__(self, path: str, delimiter: str):
        super().__init__(path)
        self.delimiter = delimiter

    def get_data(self) -> list[Host]:
        data_list = []

        with closing(open(self.path, 'r')) as file:
            file_data = csv.reader(file, delimiter=self.delimiter)
            next(file_data, None)

            for row in file_data:
                validation_results = validate_str(row[0], [ValidationTypes.NOT_EMPTY_HOST,
                                                           ValidationTypes.CORRECT_DOMAIN,
                                                           ValidationTypes.CORRECT_IP])

                is_ip = validation_results[ValidationTypes.CORRECT_IP].result
                is_domain = validation_results[ValidationTypes.CORRECT_DOMAIN].result and \
                            not validation_results[ValidationTypes.CORRECT_IP].result

                if is_ip or is_domain:
                    ports = row[1].split(',') if row[1] != '' else []
                    for i in range(len(ports)):
                        validation_results = validate_str(ports[i], [ValidationTypes.CORRECT_PORT])

                        has_key = ValidationTypes.CORRECT_PORT in validation_results.keys()
                        is_successful = validation_results[ValidationTypes.CORRECT_PORT].result

                        if has_key and not is_successful:
                            print(f'Ошибка в строке {row}: '
                                  f'{validation_results[ValidationTypes.CORRECT_PORT].message}!')
                            ports[i] = None

                    data_list.append(Host(
                        row[0] if is_domain else '',
                        [] if is_domain else [row[0]],
                        [Port(int(port), False) for port in ports if port is not None]
                    ))
                else:
                    failed_results = [item for item in validation_results.values() if not item.result]
                    print(f'Ошибка в строке {row}: {failed_results[0].message}!')

        return data_list


class JsonReader(Reader):
    def get_data(self) -> list[Host]:
        data_list = []

        with closing(open(self.path, 'r')) as file:
            file_data = json.load(file)

            for obj in file_data:
                for key, key_values in obj.items():
                    validation_results = validate_str(key, [ValidationTypes.NOT_EMPTY_HOST,
                                                            ValidationTypes.CORRECT_DOMAIN,
                                                            ValidationTypes.CORRECT_IP])

                    is_ip = validation_results[ValidationTypes.CORRECT_IP].result
                    is_domain = validation_results[ValidationTypes.CORRECT_DOMAIN].result and \
                                not validation_results[ValidationTypes.CORRECT_IP].result

                    if is_ip or is_domain:
                        values = list(key_values.values())
                        ports = values[0] if len(values) != 0 else []
                        for i in range(len(ports)):
                            validation_results = validate_str(ports[i], [ValidationTypes.CORRECT_PORT])

                            has_key = ValidationTypes.CORRECT_PORT in validation_results.keys()
                            is_successful = validation_results[ValidationTypes.CORRECT_PORT].result

                            if has_key and not is_successful:
                                print(f'Ошибка в значении {ports[i]}: '
                                      f'{validation_results[ValidationTypes.CORRECT_PORT].message}!')
                                ports[i] = None

                        data_list.append(Host(
                            key if is_domain else '',
                            [] if is_domain else [key],
                            [Port(int(port), False) for port in ports if port is not None]
                        ))
                    else:
                        failed_results = [item for item in validation_results.values() if not item.result]
                        print(f'Ошибка в ключе {key}: {failed_results[0].message}!')

        return data_list


def get_reader(params) -> Reader:
    reader = None

    if params.f == 'csv':
        reader = CsvReader(params.p, ';' if params.d is None else params.d)
    elif params.f == 'json':
        reader = JsonReader(params.p)

    return reader
