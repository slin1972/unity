# coding: utf-8
import binascii
import time

import gevent
import gevent.queue
import gevent.event
from gevent import socket
import traceback
import abc
import logging

run_log = logging.getLogger('run')
stat_log = logging.getLogger('stat')
MESSAGE_HEAD = 4


class Session:
    def __init__(self, sock, cmd_factory):
        __metaclass__ = abc.ABCMeta
        self.sock = sock
        self.idt = None

        self.is_start = False
        self.connect_time = int(time.time())
        self.last_recv_time = int(time.time())
        self._end_event = gevent.event.Event()
        self._read_thread = gevent.Greenlet(self.read_loop)
        self._write_thread = gevent.Greenlet(self.write_loop)

        self.send_queue = gevent.queue.Queue()
        self.recv_queue = gevent.queue.Queue()

        self.cmd_factory = cmd_factory

    def run(self):
        self._read_thread.start()
        self._write_thread.start()

        while True:
            ret = self._end_event.wait(10)
            if ret == True:
                run_log.error('session run  session is end')
                self.stop()
                break

            if int(time.time()) - self.last_recv_time > 300:
                run_log.error('session run  session time out')
                self.stop()
                break

    def is_end(self):
        return self._end_event.is_set()

    def stop(self):
        if not self.is_end():
            self._end_event.set()

        stat_log.info('stop session[%s]', self.get_idt())

        if self.sock:
            self.sock.close()
        run_log.info('%s sock close', self.get_idt())

        self._read_thread.kill(block=False)
        run_log.info('%s _read_thread killed', self.get_idt())
        self._write_thread.kill(block=False)
        run_log.info('%s _write_thread killed', self.get_idt())

    def get_idt(self):
        if self.idt == None:
            return ''
        return self.idt

    @abc.abstractmethod
    def recv_message(self):
        self.last_recv_time = int(time.time())

        # return msgid, data[:payload_len]

    def send_message(self, msg):
        self.send_queue.put(msg)
        return True

    def read_loop(self):
        run_log.info('read_loop  session[%s] enter read', self.get_idt())
        while True:
            data = None
            try:
                run_log.info('read_loop  wait_read session[%s]', self.get_idt())
                socket.wait_read(self.sock.fileno())
                msgid, data = self.recv_message()

                if msgid != None:
                    run_log.info('read_loop  session[%s] get msgid[%d] msg['+data+']', self.get_idt(), msgid)
                    if msgid == -1:
                        break
                else:
                    run_log.info('read_loop  session[%s] recv_message None', self.get_idt())

                if msgid in self.cmd_factory:
                    cmd_processer = self.cmd_factory[msgid]
                    resp = cmd_processer.process(data, self)

                    if resp is not None:
                        self.send_message(resp)
                        run_log.info('read_loop  session[%s] get msg[%d] resp [len:%d %s]', self.get_idt(), msgid,
                                     len(resp), resp)
                    else:
                        run_log.info('read_loop  session[%s] get msg[%d] do not resp msg', self.get_idt(), msgid)

            except Exception as msg:
                run_log.error('read_loop session[%s] socket read error:%s', self.get_idt(), str(msg))
                traceback.print_exc()
                break

            if self.is_end():
                run_log.info('read_loop session[%s] is end', self.get_idt())
                break

            if None == data:
                break
                # print 'recv:',data
                # read from socket
        self._end_event.set()
        run_log.info('read_loop  quit read')

    def write_loop(self):
        run_log.info('write_loop  session[%s] enter write', self.get_idt())
        while True:
            data = None
            try:
                data = self.send_queue.get(timeout=30)
            except Exception, e:
                pass

            if data is not None:
                run_log.info('write_loop  session[%s] send data[%s]', self.get_idt(), binascii.b2a_hex(data))
                if len(data) <= MESSAGE_HEAD:
                    run_log.error('write_loop  error msg length')
                    break
                try:
                    run_log.info('write_loop  session[%s] try write', self.get_idt())
                    socket.wait_write(self.sock.fileno(), timeout=5)

                    self.sock.sendall(data)
                    run_log.info('write_loop  session[%s]  send all end', self.get_idt())

                except Exception as msg:
                    run_log.error('write_loop  session[%s] error %s', self.get_idt(), str(msg))
                    break
            else:
                run_log.info('write_loop  session[%s] send_queue enpty', self.get_idt())

            if self.is_end():
                run_log.info('write_loop  session[%s] is end', self.get_idt())
                break

                # write to socket
        self._end_event.set()
        run_log.info('read_loop  quit write')

    @staticmethod
    @abc.abstractmethod
    def create_session(sock, head, address):
        pass
        # return data,session


'''
def create_session(sock,head,address):
    print 'hajj_band create_session'
    sock.settimeout(5)
    token,msgid,payload_length = None,None,None
    try:
        token,msgid,payload_length = unpack_head(head)
        if token is not HAJJ_BAND_TOKEN  or msgid is not HANDSHAKE_REQ_MSG:
            return None
    except Exception, e:
        print 'Exception',e
        return None

    print token,msgid,payload_length
    session = HajjBandSession(sock)
    print 'session'
    handshake_req = session.recv_handshake_req(payload_length)
    if handshake_req is None:
        return None
    print 'req'
    session.send_handshake_resp(handshake_req)
    print 'resp'
    return session
'''
