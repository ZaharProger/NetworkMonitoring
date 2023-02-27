from modules.readers import get_reader


def run(cfg):
    reader = get_reader(cfg)

    if reader is not None:
        hosts = reader.get_data()
        for host in hosts:
            print(f'[{host.host_type}] {host.name}: {host.ports}')
    else:
        print(f'Модуль для обработки файлов {cfg.f} не найден!')
