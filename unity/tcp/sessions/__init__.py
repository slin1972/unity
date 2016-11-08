# coding: utf-8
import session
import session_manager

__version__ = '0.0.1'
VERSION = tuple(map(int, __version__.split('.')))


def create_session_manager(server_name, SessionModelClass):
    g_session_manager = session_manager.SessionManager(server_name)
    g_session_manager.sessionFactory.append(SessionModelClass)

    return g_session_manager

__all__ = [
    'session_manager',
    'create_session_manager',
    'session'
]
