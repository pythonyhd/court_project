# -*- coding: utf-8 -*-
# @Time    : 2019/10/8 11:53
# @Author  : Yasaka.Yu
# @File    : court_filter.py
import re
import hashlib


# md5加密方法
def get_md5_value(_str):
    if isinstance(_str, str):
        code_url = _str.encode("utf-8")
        m = hashlib.md5()
        m.update(code_url)
        return m.hexdigest()
    else:
        return None


# 处理文书号
def __deal_with_cf_wsh(cf_wsh):
    if cf_wsh:
        cf_wsh = re.sub(r'\r|\?|\n|\t| |　', '', cf_wsh)
        cf_wsh = re.sub(r'〔|\[|【|（|﹝|{　', '(', cf_wsh)
        cf_wsh = re.sub(r'〕|]|】|）|﹞|}', ')', cf_wsh)
        return cf_wsh
    else:
        return ""


# 处理其他字段
def __deal_with_other(_str):
    if _str:
        _str = re.sub(r'\r|\?|\n|\t| |　', '', _str)
        return _str
    else:
        return ""


def cf_74_filter(item):
    """
    裁判文书排重
    :param item:
    :return:
    """
    if isinstance(item, dict):
        xq_url = item.get('xq_url')
        sj_type = item.get('sj_type', 74)
        cf_xzjg = item.get('cf_xzjg')
        oname = item.get('oname')
        if xq_url:
            if cf_xzjg:
                if oname:
                    if sj_type:
                        _str = xq_url + cf_xzjg + oname + str(sj_type)
                        return get_md5_value(_str)
                    else:
                        _str = xq_url + cf_xzjg + oname
                else:
                    _str = xq_url + cf_xzjg
                    return get_md5_value(_str)
            else:
                _str = xq_url
                return get_md5_value(_str)
        else:
            return None
    else:
        return None


def cf_75_filter(item):
    """
    开庭公告排重
    :param item:
    :return:
    """
    if isinstance(item, dict):
        xq_url = item.get('xq_url')
        sj_type = item.get('sj_type', 75)
        cf_xzjg = item.get('cf_xzjg')
        oname = item.get('oname')
        if xq_url:
            if cf_xzjg:
                if oname:
                    if sj_type:
                        _str = xq_url + cf_xzjg + oname + str(sj_type)
                        return get_md5_value(_str)
                    else:
                        _str = xq_url + cf_xzjg + oname
                else:
                    _str = xq_url + cf_xzjg
                    return get_md5_value(_str)
            else:
                _str = xq_url
                return get_md5_value(_str)
        else:
            return None
    else:
        return None


def cf_76_filter(item):
    """
    执行公告排重
    :param item:
    :return:
    """
    if isinstance(item, dict):
        xq_url = item.get('xq_url')
        sj_type = item.get('sj_type', 76)
        cf_xzjg = item.get('cf_xzjg')
        oname = item.get('oname')
        if xq_url:
            if cf_xzjg:
                if oname:
                    if sj_type:
                        _str = xq_url + cf_xzjg + oname + str(sj_type)
                        return get_md5_value(_str)
                    else:
                        _str = xq_url + cf_xzjg + oname
                else:
                    _str = xq_url + cf_xzjg
                    return get_md5_value(_str)
            else:
                _str = xq_url
                return get_md5_value(_str)
        else:
            return None
    else:
        return None


def cf_77_filter(item):
    """
    其他公告排重
    :param item:
    :return:
    """
    if isinstance(item, dict):
        xq_url = item.get('xq_url')
        sj_type = item.get('sj_type', 77)
        cf_xzjg = item.get('cf_xzjg')
        oname = item.get('oname')
        if xq_url:
            if cf_xzjg:
                if oname:
                    if sj_type:
                        _str = xq_url + cf_xzjg + oname + str(sj_type)
                        return get_md5_value(_str)
                    else:
                        _str = xq_url + cf_xzjg + oname
                else:
                    _str = xq_url + cf_xzjg
                    return get_md5_value(_str)
            else:
                _str = xq_url
                return get_md5_value(_str)
        else:
            return None
    else:
        return None


def cf_17_filter(item):
    """
    其他公告排重
    :param item:
    :return:
    """
    if isinstance(item, dict):
        xq_url = item.get('xq_url')
        sj_type = item.get('sj_type', 17)
        cf_xzjg = item.get('cf_xzjg')
        oname = item.get('oname')
        if xq_url:
            if cf_xzjg:
                if oname:
                    if sj_type:
                        _str = xq_url + cf_xzjg + oname + str(sj_type)
                        return get_md5_value(_str)
                    else:
                        _str = xq_url + cf_xzjg + oname
                else:
                    _str = xq_url + cf_xzjg
                    return get_md5_value(_str)
            else:
                _str = xq_url
                return get_md5_value(_str)
        else:
            return None
    else:
        return None


def cf_20_filter(item):
    """
    其他公告排重
    :param item:
    :return:
    """
    if isinstance(item, dict):
        xq_url = item.get('xq_url')
        sj_type = item.get('sj_type', 20)
        cf_xzjg = item.get('cf_xzjg')
        oname = item.get('oname')
        if xq_url:
            if cf_xzjg:
                if oname:
                    if sj_type:
                        _str = xq_url + cf_xzjg + oname + str(sj_type)
                        return get_md5_value(_str)
                    else:
                        _str = xq_url + cf_xzjg + oname
                else:
                    _str = xq_url + cf_xzjg
                    return get_md5_value(_str)
            else:
                _str = xq_url
                return get_md5_value(_str)
        else:
            return None
    else:
        return None


def cf_54_filter(item):
    """
    行政处罚通知书
    :param item:
    :return:
    """
    if isinstance(item, dict):
        xq_url = item.get('xq_url')
        sj_type = item.get('sj_type', 20)
        cf_xzjg = item.get('cf_xzjg')
        oname = item.get('oname')
        if xq_url:
            if cf_xzjg:
                if oname:
                    if sj_type:
                        _str = xq_url + cf_xzjg + oname + str(sj_type)
                        return get_md5_value(_str)
                    else:
                        _str = xq_url + cf_xzjg + oname
                else:
                    _str = xq_url + cf_xzjg
                    return get_md5_value(_str)
            else:
                _str = xq_url
                return get_md5_value(_str)
        else:
            return None
    else:
        return None


def filter_factory(item):
    sj_type = item.get('sj_type')
    if sj_type == 74:
        return cf_74_filter(item)
    elif sj_type == 75:
        return cf_75_filter(item)
    elif sj_type == 76:
        return cf_76_filter(item)
    elif sj_type == 77:
        return cf_77_filter(item)
    elif sj_type == 17:
        return cf_17_filter(item)
    elif sj_type == 20:
        return cf_20_filter(item)
    elif sj_type == 54:
        return cf_54_filter(item)