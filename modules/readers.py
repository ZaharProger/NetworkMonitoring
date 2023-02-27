import csv
import json
from abc import ABC, abstractmethod
from .validation import ValidationTypes, validate_str


class Reader(ABC):
    def __init__(self, path: str):
        self.path = path

    @abstractmethod
    def get_data(self) -> dict:
        ...


class CsvReader(Reader):
    def __init__(self, path: str, delimiter: str):
        super().__init__(path)
        self.delimiter = delimiter

    def get_data(self) -> dict:
        data_dict = {}

        with open(self.path, 'r') as file:
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
                    data_dict[row[0]] = row[1].split(',') if row[1] != '' else []
                else:
                    failed_results = [item for item in validation_results.values() if not item.result]
                    print(f'Ошибка в строке {row}: {failed_results[0].message}!')

        return data_dict


class JsonReader(Reader):
    def get_data(self) -> dict:
        data_dict = {}

        with open(self.path, 'r') as file:
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
                        data_dict[key] = values[0] if len(values) != 0 else []
                    else:
                        failed_results = [item for item in validation_results.values() if not item.result]
                        print(f'Ошибка в ключе {key}: {failed_results[0].message}!')

        return data_dict
