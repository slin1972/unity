#coding: utf8

'''

2015-09-29
用于mysql的连接池 
'''
import gevent
import pymysql
import random
import time
import logging
logger = logging.getLogger()

def escape(data):
    return pymysql.escape_string(data)

class MySqlPool:
    def __init__(self, max_conn_count, max_wait_conn_sec, **args):
        self.conn_args = args
        self.max_conn_count = max_conn_count
        self.conn2status = {}
        self.time2status = {}
        self.max_wait_conn_sec = max_wait_conn_sec

    def __get_conn(self):
        conn_list = [c for c in self.conn2status if self.conn2status[c] == 0 ]
        if len(conn_list) > 0:
            conn = random.choice(conn_list)
            self.conn2status[conn] = 1
            return conn

        if len(self.conn2status) < self.max_conn_count:
            conn = pymysql.connect(**self.conn_args)
            self.conn2status[conn] = 1 
            return conn
        return None 

    def ensure_conn(self):
        now = int(time.time())
        del_list = []
        for c in self.conn2status:
            if self.conn2status[c] == 0 and now - self.time2status[c] > 10 * self.max_wait_conn_sec:
                del_list.append(c)

        for c in del_list:
            self.free(c)

    def get_conn(self):
        self.ensure_conn()
        for i in range(0, 10 * self.max_wait_conn_sec):
            conn = self.__get_conn()
            if conn <> None:
                return conn
            gevent.sleep(0.1)
        return None

    def reuse(self, conn):
        if conn in self.conn2status:
            self.conn2status[conn] = 0
            self.time2status[conn] = int(time.time())
 
    def free(self, conn):
        if conn <> None:
            conn.close()
            del self.time2status[conn]
            del self.conn2status[conn]


class MyCursor:
    def __init__(self, connpool):
        self.connpool = connpool
        self.conn = None
        self.cr = None

    def make_cr(self):
        self.conn = self.connpool.get_conn()
        if self.conn != None:
            self.cr = self.conn.cursor()
        logger.debug('MyCursor.__init__: %s' % str(self.cr))

        return self.cr != None

    def save(self):
        self.conn.commit()

    def __enter__(self):
        return self.cr.__enter__() 

    def __exit__(self, exc_type, exc_val, exc_tb):
        if self.conn is None:
            return
        if exc_val <> None:
            self.connpool.free(self.conn)
        else:
            self.connpool.reuse(self.conn)
            
    def __del__(self):
        logger.debug('MyCursor.__del__: %s' % str(self.cr))
        if self.cr != None:
            self.conn.rollback()
            self.cr.close()
            self.connpool.reuse(self.conn)

    def __getattr__(self, name):
        return getattr(self.cr, name)


