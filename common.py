# coding: utf-8
import sys, time, os
import datetime
import math
import urlparse
import hashlib


def md5(src):
    m2 = hashlib.md5()
    m2.update(src)
    return m2.hexdigest()


def safe_get(data, field, default_value ):
    if field not in data:
        return default_value;
    return data[field]


def get_url_param(param_s):
    return dict([(k, v[0]) for k, v in urlparse.parse_qs(param_s).items()])


def get_now_datetime(format="%Y-%m-%d %H:%M:%S"):
    now = datetime.datetime.now()
    return now.strftime(format)



def get_datetimeobj(date_time_str, format):
    t = datetime.datetime.strptime(date_time_str, format)
    return t


def get_timestamp_by_datetime(str_date):
    timeArray = time.strptime(str_date, "%Y-%m-%d %H:%M:%S")
    timeStamp = int(time.mktime(timeArray))
    return timeStamp


def get_timestamp(str_date, format):
    print str_date, format
    timeArray = time.strptime(str_date, format)
    timeStamp = int(time.mktime(timeArray))
    return timeStamp


def get_datetime(time_stamp, format):
    ltime=time.localtime(time_stamp)
    timeStr=time.strftime(format, ltime)
    return timeStr

def get_datetime_by_timestamp(time_stamp):
    ltime=time.localtime(time_stamp)
    timeStr=time.strftime("%Y-%m-%d %H:%M:%S", ltime)
    return timeStr

def get_datetimestr(datetime, format):
    return datetime.strftime(format)


def ApplicationInstance(file=None):
    import platform
    if (platform.platform()).count("Windows") > 0:
        print "Current system is windows, skip ApplicationInstance..."
        return
    else:
        import fcntl
        global pidfile
        if file is None:
            pidfile = open(os.path.realpath(__file__), "r")
        else:
            pidfile = open(os.path.realpath(file), "r")
        try:
            fcntl.flock(pidfile, fcntl.LOCK_EX | fcntl.LOCK_NB) #创建一个排他锁,并且所被锁住其他进程不会阻塞
        except:
            print "another instance is running..."
            sys.exit(1)


def rad(d):
   return d * math.pi / 180.0


def distance(lat1,lng1,lat2,lng2):  
    radlat1=rad(lat1)  
    radlat2=rad(lat2)  
    a=radlat1-radlat2  
    b=rad(lng1)-rad(lng2)  
    s=2*math.asin(math.sqrt(math.pow(math.sin(a/2),2)+math.cos(radlat1)*math.cos(radlat2)*math.pow(math.sin(b/2),2)))  
    earth_radius=6378.137  * 1000
    s=s*earth_radius  
    if s<0:  
        return -s  
    else:  
        return s  


class Point:
    def __init__(self,x,y):
        self.x = x
        self.y = y


def current_timesecond():
    return int(time.time())



def isPtInPoly(point,graph):
    count = len(graph)
    if count < 3:
        return False

    s = 0
    x1,y1,x2,y2 = 0,0,0,0
    for i in range(count-1):
        x1 = graph[i].x
        y1 = graph[i].y
        x2 = graph[(i+1)%count].x
        y1 = graph[(i+1)%count].y

        if (((point.y >= y1) and (point.y < y2)) or ((point.y >= y2) and (point.y < y1))):
            if y1 != y2:
                x = x1 - ((x1 - x2) * (y1 - point.y)) / (y1 - y2);
                if x < point.x:
                    s+=1

    if s%2 != 0:
        return True
    return False

if __name__ == '__main__':
    print md5(md5(md5("test123")[:16]))
