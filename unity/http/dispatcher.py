# coding: utf-8

import logging
import traceback
import unity.core

from unity.core import CommonResult

logger = logging.getLogger()
import time, urllib, json


def default_cmd_handle(env, start_response):
    begin_time = time.time()
    time.localtime()
    relate_path = env['PATH_INFO'][1:]
    method = env['REQUEST_METHOD']
    query_string = env["QUERY_STRING"]
    query_string = urllib.unquote(query_string)
    query_dict = {}
    if query_string.strip() != "":
        query_arr = query_string.split("&")
        if len(query_arr) > 0:
            for query in query_arr:
                dict = query.split("=")
                if len(query_arr) > 0:
                    query_dict[dict[0].strip()] = dict[1].strip()
    try:
        if method == "POST":
            request_body_size = int(env.get('CONTENT_LENGTH', 0))
            params = env['wsgi.input'].read(request_body_size)
            logger.info("[Request]---%s---%s" % (relate_path, repr(params)))
            result = execute(relate_path, params)
        else:
            logger.info("[Request]---%s---%s" % (relate_path, query_string))
            result = execute(relate_path, query_dict)
    except Exception:
        logger.error(traceback.format_exc())
        result = unity.core.CommonResult(999, None, "Server exception.")
    start_response("200 OK", [('Content-Type', 'application/json'), ("Access-Control-Allow-Origin", "*")])
    response = json.dumps(result, default=lambda obj: obj.__dict__)
    end_time = time.time()
    logger.info("[Response]---%d---%s---%s" % (int((end_time - begin_time) * 1000), relate_path, response))
    return response


def execute(relate_path, request_body):
    app = path_handler.get(relate_path)
    if app is None:
        logger.warn("%s%s" % ("[Nomapping]No mapping hander for path :", relate_path))
        return CommonResult(100, None, "No mapping hander.")
    if str(type(app)) == "<type 'function'>":
        result = app(request_body)
    else:
        result = app.handle(request_body)
    if result is None or result.code != 0:
        logger.warn("%s[%s]---%s---%s" % ("[Nodata]", result.code, relate_path, request_body))
    return result

path_handler = {}


def init_path_handler(path_handler_param):
    global path_handler
    path_handler = path_handler_param

