from modules.loggers import ConsoleLogger, use_logger
from modules.network import NetworkService, DnsResolver, Pinger, PortScanner
from modules.readers import get_reader


def run(cfg):
    console_logger = ConsoleLogger()
    messages = []
    reader = get_reader(cfg)

    if reader is not None:
        reader.logger = console_logger

        print('Чтение файла...')
        hosts = reader.get_data()

        print('Сканирование адресов из файла...')
        network_service = NetworkService(dns_resolver=DnsResolver(),
                                         pinger=Pinger(),
                                         port_scanner=PortScanner())

        for host in hosts:
            messages.extend(network_service.scan_host(host))
    else:
        messages = [f"Модуль для обработки файлов {cfg.f} не найден!"]

    use_logger(console_logger, messages)
