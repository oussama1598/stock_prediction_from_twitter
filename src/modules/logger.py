import logging
import os

from colorlog import ColoredFormatter


class Logger(logging.Logger):
    def __init__(self, name):
        super().__init__(name)

        self.setLevel(logging.DEBUG)

        log_stream = logging.StreamHandler()
        log_stream.setLevel(logging.DEBUG)

        if os.getenv('COLORED_OUTPUT') == '1':
            log_stream.setFormatter(
                ColoredFormatter(
                    '%(log_color)s%(asctime)s%(reset)s | %(log_color)s%(name)s%(reset)s '
                    '| %(log_color)s%(levelname)s%(reset)s | %(log_color)s%(message)s%(reset)s'
                )
            )
        else:
            log_stream.setFormatter(
                logging.Formatter(
                    '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
                )
            )

        self.addHandler(log_stream)
