import csv
import json
from abc import ABC, abstractmethod
from contextlib import closing

from .entities import Host
from .loggers import Logger, use_logger
from .validation import ValidationTypes, validate_str


class Reader(ABC):
    def __init__(self, path: str, logger: Logger = None):
        self._path = path
        self.logger = logger

    @property
    def path(self):
        return self._path

    @path.setter
    def path(self, path: str):
        self._path = path

    @abstractmethod
    def get_data(self) -> list[Host]:
        ...

    def _map_item(self, host_str: str, port_list: list[str]) -> Host:
        mapped_item = None
        messages = []

        validation_results = validate_str(host_str, [ValidationTypes.NOT_EMPTY_HOST,
                                                     ValidationTypes.CORRECT_DOMAIN,
                                                     ValidationTypes.CORRECT_IP])

        is_ip = validation_results[ValidationTypes.CORRECT_IP].result
        is_domain = validation_results[ValidationTypes.CORRECT_DOMAIN].result and \
                    not validation_results[ValidationTypes.CORRECT_IP].result

        if is_ip or is_domain:
            for i in range(len(port_list)):
                validation_results = validate_str(port_list[i], [ValidationTypes.CORRECT_PORT])
                if not validation_results[ValidationTypes.CORRECT_PORT].result:
                    messages.extend([f'Ошибка в элементе {port_list[i]}: '
                                     f'{validation_results[ValidationTypes.CORRECT_PORT].message}!'])
                    port_list[i] = None

            mapped_item = Host(
                host_str if is_domain else '',
                [] if is_domain else [host_str],
                [int(port) for port in port_list if port is not None]
            )
        else:
            failed_results = [item for item in validation_results.values() if not item.result]
            messages.extend([f'Ошибка в элементе {host_str}: {failed_results[0].message}!'])

        use_logger(self.logger, messages)

        return mapped_item


class CsvReader(Reader):
    def __init__(self, path: str, delimiter: str):
        super().__init__(path)
        self.__delimiter = delimiter

    @property
    def delimiter(self):
        return self.__delimiter

    @delimiter.setter
    def delimiter(self, delimiter: str):
        self.__delimiter = delimiter

    def get_data(self) -> list[Host]:
        data_list = []

        with closing(open(self.path, 'r')) as file:
            file_data = csv.reader(file, delimiter=self.delimiter)
            next(file_data, None)

            for row in file_data:
                mapped_item = self._map_item(row[0], row[1].split(',') if row[1] != '' else [])
                if mapped_item is not None:
                    data_list.append(mapped_item)

        return data_list


class JsonReader(Reader):
    def get_data(self) -> list[Host]:
        data_list = []

        with closing(open(self.path, 'r')) as file:
            file_data = json.load(file)

            for obj in file_data:
                for key, key_values in obj.items():
                    values = list(key_values.values())
                    ports = values[0] if len(values) != 0 else []

                    mapped_item = self._map_item(key, ports)

                    if mapped_item is not None:
                        data_list.append(mapped_item)

        return data_list


def get_reader(params) -> Reader:
    reader = None

    if params.f == 'csv':
        reader = CsvReader(params.p, ';' if params.d is None else params.d)
    elif params.f == 'json':
        reader = JsonReader(params.p)

    return reader
