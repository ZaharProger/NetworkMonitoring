from modules.readers import CsvReader, JsonReader


def run(path: str):
    reader = CsvReader(path, ';') #JsonReader(path)
    data = reader.get_data()

    for key, value in data.items():
        print(f'{key}: {value}')
