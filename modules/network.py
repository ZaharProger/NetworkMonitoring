from pythonping import ping
from datetime import datetime
from abc import ABC, abstractmethod
from contextlib import closing
import socket
from time import time

from modules.entities import Host


class DnsResolver:
    @staticmethod
    def resolve(name: str) -> list[str]:
        return socket.gethostbyname_ex(name)[2]


class Scanner(ABC):
    def __init__(self, log_format: str = '%Y-%m-%d %H:%M:%S:%f'):
        self._log_format = log_format

    @abstractmethod
    def scan(self, host: Host):
        ...


class PortScanner(Scanner):
    def scan(self, host: Host) -> list[str]:
        messages = []
        with closing(socket.socket(socket.AF_INET, socket.SOCK_STREAM)) as sock:
            for address in host.ip_addresses:
                for port in host.ports:
                    start_time = time() * 1000
                    port.is_opened = sock.connect_ex((address, port.value)) == 0
                    end_time = time() * 1000

                    current_time = datetime.now().strftime(self._log_format)
                    rtt = end_time - start_time

                    messages.append(f'{current_time} {host.domain_name} {address} {rtt}ms '
                                    f"{port.value} {'Opened' if port.is_opened else 'Unknown'}")

        return messages


class Pinger(Scanner):
    def scan(self, host: Host) -> list[str]:
        messages = []
        for address in host.ip_addresses:
            start_time = time() * 1000
            results = ping(address, count=1, size=4)
            end_time = time() * 1000

            current_time = datetime.now().strftime(self._log_format)
            rtt = end_time - start_time

            messages.append(f'{current_time} {host.domain_name} {address} {rtt}ms '
                            f'{results.stats_packets_sent} packets sent '
                            f'{results.stats_packets_returned} packets returned ({results.stats_success_ratio * 100}%) '
                            f'{results.stats_packets_lost} packets lost ({results.stats_lost_ratio * 100}%)')

        return messages


class NetworkService:
    def __init__(self, dns_resolver: DnsResolver, scanners: list[Scanner]):
        self.__dns_resolver = dns_resolver
        self.__scanners = scanners

    def monitor(self, host: Host) -> list[str]:
        if host.domain_name != '' and self.__dns_resolver is not None:
            host.ip_addresses = self.__dns_resolver.resolve(host.domain_name)

        messages = [f'{host.domain_name} {host.ip_addresses} {[port.value for port in host.ports]}']
        for scanner in self.__scanners:
            if scanner is not None:
                messages.extend(scanner.scan(host))

        return messages
