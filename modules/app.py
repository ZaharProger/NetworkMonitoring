from modules.entities import HostTypes
from modules.readers import get_reader


def run(cfg):
    reader = get_reader(cfg)

    if reader is not None:
        hosts = reader.get_data()

        for host in hosts:
            if host.host_type == HostTypes.DOMAIN:
                pass
            elif host.host_type == HostTypes.IP:
                pass
    else:
        print(f"Модуль для обработки файлов {cfg.f} не найден!")
