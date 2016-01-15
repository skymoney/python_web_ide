#-*- coding:utf-8 -*-

import math
import pytz

from idev2.settings import ITEMS_PER_PAGE
from idev2.settings import TIME_ZONE

def get_current_page(page_str):
    try:
        page = int(page_str)
    except Exception, e:
        page = 1

    if page < 1:
        page = 1

    return page


def get_total_page(num):
    return int(math.ceil(num*1.0 /ITEMS_PER_PAGE)) \
            if num > 0 else 1


def date_to_string(time_data):
    return time_data.astimezone(pytz.timezone(TIME_ZONE)).strftime('%Y-%m-%d %H:%M:%S')