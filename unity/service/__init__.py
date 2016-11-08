# coding: utf8

import mysql_service
import redis_service

__version__ = '0.0.1'
VERSION = tuple(map(int, __version__.split('.')))


def init_redis_service(host, port, db, passwd):
    redis_service.init(host, port, db, passwd)


def init_mysql_service(connection_url):
    mysql_service.init_mysql(connection_url)

__all__ = [
    "mysql_service",
    "redis_service"
]



