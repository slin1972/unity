# coding: utf-8
import logging  
import logging.config


g_logger = {}
LOG_PATH = '/logs/'


def init_log():
    format='%(asctime)s %(filename)s[line:%(lineno)d] %(levelname)s %(message)s'
    datefmt='%Y-%m-%d %H:%M:%S'

    formatter = logging.Formatter(format,datefmt)

    rotatinghandler = logging.handlers.RotatingFileHandler(LOG_PATH+'test_rotating.log', maxBytes = 1024*1024, backupCount = 5)
    rotatinghandler.setFormatter(formatter)
    info_log = logging.getLogger('run_info')
    info_log.addHandler(rotatinghandler) 
    info_log.setLevel(logging.DEBUG)  
    g_logger['run_info'] = info_log

    timehandler = logging.handlers.TimedRotatingFileHandler(LOG_PATH+'test_time.log',when='h',interval=1, backupCount = 24*7)
    timehandler.setFormatter(formatter)
    stat_log = logging.getLogger('stat')
    stat_log.addHandler(timehandler) 
    stat_log.setLevel(logging.DEBUG)  
    g_logger['stat'] = stat_log


def get_logger(name):
    if name in g_logger:
        return g_logger[name]
    return None
