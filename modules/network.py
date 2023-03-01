from pythonping import ping
from datetime import datetime
from contextlib import closing
from abc import ABC, abstractmethod
import socket
from urllib.request import urlopen
from time import time

from .entities import Host


class Scanner(ABC):
    @abstractmethod
    def scan(self, host: Host) -> list[str]:
        ...


class DnsResolver(Scanner):
    def scan(self, host: Host) -> list[str]:
        incorrect_domain = False

        if host.domain_name != '':
            try:
                host.ip_addresses = socket.gethostbyname_ex(host.domain_name)[2]
            except socket.gaierror:
                incorrect_domain = True

        messages = [f'\n{host.domain_name} {host.ip_addresses} {host.ports}']
        if incorrect_domain:
            messages.append(f'Ошибка в элементе {host.domain_name}: Не удалось разрешить доменное имя!')

        return messages


class PortScanner(Scanner):
    def scan(self, host: Host) -> list[str]:
        messages = []
        with closing(socket.socket(socket.AF_INET, socket.SOCK_STREAM)) as sock:
            for address in host.ip_addresses:
                for port in host.ports:
                    start_time = time() * 1000
                    is_opened = sock.connect_ex((address, port)) == 0
                    end_time = time() * 1000

                    current_datetime = datetime.now().strftime('%Y-%m-%d %H:%M:%S:%f')
                    rtt = round(end_time - start_time, 2)

                    messages.append(f'{current_datetime} {host.domain_name} {address} {rtt}ms '
                                    f"{port} {'Opened' if is_opened else 'Unknown'}")

        return messages


class Pinger(Scanner):
    def __init__(self, packets_amount: int = 4, packet_size: int = 4, timeout: int = 3):
        self.__packets_amount = packets_amount
        self.__packet_size = packet_size
        self.__timeout = timeout

    @property
    def packets_amount(self):
        return self.__packets_amount

    @packets_amount.setter
    def packets_amount(self, packets_amount: int):
        if packets_amount > 0:
            self.__packets_amount = packets_amount

    @property
    def packet_size(self):
        return self.__packet_size

    @packet_size.setter
    def packet_size(self, packet_size: int):
        if packet_size > 0:
            self.__packet_size = packet_size

    @property
    def timeout(self):
        return self.__timeout

    @timeout.setter
    def timeout(self, timeout: int):
        if timeout > 0:
            self.__timeout = timeout

    def scan(self, host: Host) -> list[str]:
        messages = []
        for address in host.ip_addresses:
            for i in range(self.__packets_amount):
                results = ping(address, count=1, size=self.__packet_size, timeout=self.__timeout)
                current_datetime = datetime.now().strftime('%Y-%m-%d %H:%M:%S:%f')

                for result in results:
                    messages.append(f'{current_datetime} {host.domain_name} {address} {result.time_elapsed_ms}ms '
                                    f'{results.stats_packets_sent} packets sent '
                                    f'{results.stats_packets_returned} packets returned '
                                    f'({results.stats_success_ratio * 100}%) '
                                    f'{results.stats_packets_lost} packets lost ({results.stats_lost_ratio * 100}%) '
                                    f"{'Success' if result.error_message is None else result.error_message}")

        return messages


class NetworkService:
    def __init__(self, dns_resolver: DnsResolver = None, pinger: Pinger = None, port_scanner: PortScanner = None):
        self.dns_resolver = dns_resolver
        self.pinger = pinger
        self.port_scanner = port_scanner

    @staticmethod
    def check_connection() -> bool:
        try:
            urlopen('https://google.com')
            is_connected = True
        except:
            is_connected = False

        return is_connected

    def scan_host(self, host: Host) -> list[str]:
        messages = []

        if NetworkService.check_connection():
            if self.dns_resolver is not None:
                messages.extend(self.dns_resolver.scan(host))

            if len(host.ports) == 0 and self.pinger is not None:
                messages.extend(self.pinger.scan(host))
            elif self.port_scanner is not None:
                messages.extend(self.port_scanner.scan(host))
        else:
            messages.append('\nОтсутствует подключение к интернету!')

        return messages
