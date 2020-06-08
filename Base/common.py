import datetime
from typing import Union

from QitianSDK import QitianManager
from SmartDjango import NetPacker

from Config.models import Config, CI

NetPacker.set_mode(debug=True)
NetPacker.customize_http_code(fixed_http_code=200)

QITIAN_APP_ID = Config.get_value_by_key(CI.QITIAN_APP_ID)
QITIAN_APP_SECRET = Config.get_value_by_key(CI.QITIAN_APP_SECRET)
WX_APP_ID = Config.get_value_by_key(CI.WX_APP_ID)
WX_APP_SECRET = Config.get_value_by_key(CI.WX_APP_SECRET)

SECRET_KEY = Config.get_value_by_key(CI.PROJECT_SECRET_KEY)
JWT_ENCODE_ALGO = Config.get_value_by_key(CI.JWT_ENCODE_ALGO)
HOST = Config.get_value_by_key(CI.HOST)

DEFAULT_SPACE_COVER = 'https://image.6-79.cn/rizya/default-space-cover.jpg?' \
                      'imageMogr2/auto-orient/thumbnail/600x/blur/1x0/quality/75'

DEV_MODE = True


def time_dictor(v):
    if isinstance(v, datetime.datetime):
        return v.timestamp()
    return v


def int_or_float(number):
    try:
        number = int(number)
    except Exception:
        number = float(number)
    return number


def last_timer(last):
    if last == 0:
        return datetime.datetime.now()
    else:
        return datetime.datetime.fromtimestamp(last)


def boundary(max_=None, min_=None):
    def processor(value):
        value = int(value)
        if max_ is not None and value > max_:
            value = max_
        if min_ is not None and value < min_:
            value = min_
        return value
    return processor
