#-*- coding:utf-8 -*-


def get_current_page(page_str):
    try:
        page = int(page_str)
    except Exception, e:
        page = 1

    if page < 1:
        page = 1

    return page