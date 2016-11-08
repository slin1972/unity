# coding: utf-8

from unity.core import CommonResult
import logging
import gevent

run_log = logging.getLogger('run')
stat_log = logging.getLogger('stat')


class SessionManager:
    def __init__(self, server_identify):
        self.sessions = {}
        self.server_identify = server_identify
        self.sessionFactory = []

    def create_session(self, sock, address):
        run_log.info('create_session address[%s]', str(address))

        head = ''
        for SessionModelClass in self.sessionFactory:
            session, data = SessionModelClass.create_session(sock, head, address)
            head = data
            if session is not None:
                if session.get_idt() in self.sessions:
                    run_log.error('session[%s] already connect,  stop first ', session.get_idt())
                    self.sessions[session.get_idt()].stop()
                    self.remove_session(session.get_idt())
                self.sessions[session.get_idt()] = session
                self.sessions[session.get_idt()].create_finished()
                return session
        return None

    def remove_session(self, idt):
        if idt not in self.sessions:
            return False

        if self.sessions[idt].is_end():
            run_log.info('remove session[%s]', idt)
            session = self.sessions[idt]
            del (self.sessions[idt])
            session.remove_finished()
        else:
            run_log.warn('session[%s] not end,  do not remove ', idt)
        return True

    def send_message(self, idt, msg_id, data):
        if idt not in self.sessions:
            return False
        session = self.sessions[idt]
        session.send_message(msg_id, data)

    def handle_cmd(self, idt, func_name, params):

        # 判断idt是否多个
        if idt.count(",") > 0:
            idts = idt.split(",")
            for id in idts:
                gevent.spawn(self.handle_cmd2, id, func_name, params)
            return CommonResult(0, None, "ok")
        else:
            return self.handle_cmd2(idt, func_name, params)

    def handle_cmd2(self, idt, func_name, params):
        if idt not in self.sessions:
            return CommonResult(-1, None, 'no this device')

        session = self.sessions[idt]

        if not hasattr(session, "user"):
            return CommonResult(-1, None, 'this device have not login.')

        # if not func_name.startswith('device_'):
        #    return CommonResult(-2, None, 'do not allow this cmd')

        if not hasattr(session, func_name):
            return CommonResult(-3, None, 'no this cmd')

        func = getattr(session, func_name)
        result = func(*params)
        return CommonResult(0, result, "ok")
