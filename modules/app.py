from modules.network import NetworkService, DnsResolver, Pinger, PortScanner
from modules.readers import get_reader


def run(cfg):
    reader = get_reader(cfg)

    if reader is not None:
        hosts = reader.get_data()
        network_scanner = NetworkService(DnsResolver(), [Pinger(), PortScanner()])
        messages = []

        for host in hosts:
            messages = network_scanner.monitor(host)
    else:
        messages = [f"Модуль для обработки файлов {cfg.f} не найден!"]

    print('\n'.join(messages))
