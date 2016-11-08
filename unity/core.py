# coding: utf-8


class CommonResult:
    def __init__(self, code, data=None, msg=None):
        self.code = code
        if data is not None:
            self.data = data
        if msg is not None:
            self.msg = msg
        if self.code == 0:
            self.ok = True
        else:
            self.ok = False
OK = CommonResult(0, None, "OK")

