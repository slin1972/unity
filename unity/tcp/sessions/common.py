# coding: utf-8
import logging
import struct

run_log = logging.getLogger('run')
stat_log = logging.getLogger('stat')


def recv_n(sock, length):
    data = ''
    need = length
    need_all = length
    while need > 0:
        data_get = sock.recv(need)
        if len(data_get) is 0:
            print 'recv error'
            return None
        data += data_get
        if len(data) is need_all:
            break
        else:
            need = need_all - len(data)

    return data


def memcpy(src):
    if src is not None:
        fmt = '%ds' % len(src)
        data = struct.pack(fmt, src)
        return data
    else:
        return None

