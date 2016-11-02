# coding: utf-8
import mysql
import traceback
import re
import logging

g_db_pool = None
logger = logging.getLogger()


def init_mysql(connection_url):
    no = connection_url.split("://")[0]
    user = connection_url.split("://")[1].split(":")[0]

    passwdHost = connection_url.split("://")[1].split(":")[1].split("@")
    if len(passwdHost) == 2:
        passwd = passwdHost[0]
        host = passwdHost[1]
    elif len(passwdHost) == 3:
        passwd = passwdHost[0] + '@' + passwdHost[1]
        host = passwdHost[2]
    port = connection_url.split("://")[1].split(":")[2].split("/")[0]
    port = int(port)
    db = connection_url.split("://")[1].split(":")[2].split("/")[1].split("?")[0]
    charset = connection_url.split("://")[1].split(":")[2].split("/")[1].split("?")[1].split("=")[1]
    print no, user, passwd, host, port, db, charset
    global g_db_pool
    g_db_pool = mysql.MySqlPool(max_conn_count=10, \
    max_wait_conn_sec=6, user=user, passwd=passwd, host=host, port=port, db=db, charset=charset)


def get_mysql_client():
    m = mysql.MyCursor(connpool=g_db_pool)
    ret = m.make_cr()
    if ret:
        return m
    else:
        return None


def get_str(r):
    if r is None:
        return 'None'
    return str(r)


class MysqlExcuter:
    def __init__(self):
        self.client = get_mysql_client()

    def execute_update(self, sql, params=None):
        logger.info('sql: %s' % sql)
        row = self.client.execute(sql)
        return row

    def commit(self):
        self.client.save()

    def execute_query(self, sql, params=None, type=tuple, single=False):
        try:
            logger.info('sql: %s' % sql)
            self.client.execute(sql)
            r = self.client.fetchall()
            if len(r) == 0:
                result = r
            elif type == dict:
                s = re.compile("select.*?from").findall(sql)
                if len(s) > 0:
                    s = s[0]
                    s = s.replace("select", "").replace("from", "")
                    arr = s.split(",")
                    list = []
                    for obj in r:
                        obj_arr = {}
                        for i in range(0, len(arr)):
                            obj_arr[arr[i].strip()] = obj[i]
                        list.append(obj_arr)
                    result = list
                else:
                    result = r
            else:
                result = r
            if len(result) == 0:
                return None
            elif len(result) == 1 and single:
                return result[0]
            else:
                return result
        except Exception:
            print ('error %s' % traceback.format_exc())
            return None

