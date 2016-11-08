import urllib2
import logging
import time
import cookielib
logger = logging.getLogger()
req_record = {

}

cookieJar = cookielib.CookieJar()
opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(cookieJar))


class HttpUtil:
    def __init__(self):
        pass

    @staticmethod
    def http_send(url, body=None, headers=None, caller=None):
        startTime = time.time()
        log = "[HTTP] "
        if caller is not None:
            log += (caller+" ")
        if body is not None:
            req = urllib2.Request(url, body)
            log += "POST "
            log += (url+" ")
            log += ("'"+body+"' ")
        else:
            req = urllib2.Request(url)
            log += "GET "
            log += (url+" ")
        if headers is not None:
            for key in headers:
                req.add_header(key, headers[key])
        req.add_header('User-Agent', 'elife-client')
        error = None
        try:
            response = opener.open(req, timeout=5).read()
            log += "200 "
        except Exception, e:
            error = e
            if hasattr(e, "code"):
                log += ("%d " % e.code)
            else:
                log += ("%d " % 500)
        endTime = time.time()
        log += ("%d " % ((endTime-startTime)*1000))
        if error is None:
            log += ("'"+("".join(response.split())+" ")+"'")
        logger.info(log)
        if error:
            raise e
        return response
if __name__ == '__main__':
    try:
        response = HttpUtil.http_send("http://baidu.com", "ttt",{"a":"bbbb"}, caller="push")
    except:
        pass
        import traceback
        traceback.print_exc()

