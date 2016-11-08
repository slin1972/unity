# coding: utf-8
import logging

logger = logging.getLogger()


pool = None


def init(host, port, db, passwd):
    import redis
    global pool
    pool = redis.ConnectionPool(host=host, port=port, db=db, password=passwd, max_connections=3)


def get_redis_client():
    import redis
    r = redis.Redis(connection_pool=pool)
    # print r.ping()
    return r


class RedisExcuter:
    def __init__(self):
        self.client = get_redis_client()
        self.stat_log = logger

    def hset(self, name, key, value):
        self.client.hset(name, key, value)

    def hget(self, name, key):
        return self.client.hget(name, key)

    def hincrby(self, name, key, amount=1):
        return self.client.hincrby(name, key, amount)

    def hmget(self, name, keys):
        return self.client.hmget(name, keys)

