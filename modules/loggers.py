from abc import ABC, abstractmethod


class Logger(ABC):
    def __init__(self):
        self._messages = []

    @property
    def messages(self):
        return self._messages

    @messages.setter
    def messages(self, messages: list[str]):
        self._messages.extend(messages)

    def clear(self):
        self._messages = []

    @abstractmethod
    def perform_logging(self):
        ...


class ConsoleLogger(Logger):
    def perform_logging(self):
        print('\n'.join(self._messages))


def use_logger(logger: Logger, data: list[str]):
    if logger is not None and len(data) != 0:
        logger.messages = data
        logger.perform_logging()
        logger.clear()
