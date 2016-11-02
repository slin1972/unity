# coding: utf-8
import basic_logger

__version__ = '0.0.1'
VERSION = tuple(map(int, __version__.split('.')))

__all__ = [
    'basic_logger',
]


def init_log():
    basic_logger.init_log()