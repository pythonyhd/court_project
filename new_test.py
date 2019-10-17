# -*- coding: utf-8 -*-
# @Time    : 2019/10/8 11:10
# @Author  : Yasaka.Yu
# @File    : new_test.py
import time
from retry import retry
import re


st = '原告金碧物业有限公司哈尔滨分公司'
if '原告' in st:
    data = st.replace('原告', '')
else:
    data = ''
print(data)
timea = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))
print(type(timea))
print(timea)

aaa = '刘国凡身份证号码452225196510124232）：本院受理原告苏正求诉被告刘国凡民间借贷纠纷一案，，已审理终结。现依法向你们公告送达湘1381民初516号民事判决书，判决如下：限被告刘国凡于本判决生效之日起五日内偿还原告苏正求借款本金392000元并支付利息（利息以实欠借款本金为基准，自2008年12月1日按年利率2%支付至借款本金偿清之日止）；2、驳回原告苏正求的其余诉讼请求。本案案件受理费7300元，财产保全费3020元，公告费560元，合计10880元，由被告刘国凡负担。自公告之日起，60日内来本院领取民事判决书，逾期则视为送达。如不服本判决，可在公告期满后15日内，向本院递交上诉状及副本，上诉于湖南省娄底市中级人民法院。逾期本判决即发生法律效力。'


def get_cf_wsh(txt):
    """
    提取文书号
    :param txt:
    :return:
    """
    if txt:
        data = re.search(r'公告送达(（.*?号)', txt)
        if data:
            return data.group(1)
        data = re.search(r'(（.*?号)', txt)
        if data:
            return data.group(1)
        else:
            return '（打啊 等待是是否死的都是哈哈'
    else:
        return ""


def get_cf_xzjg(txt):
    """
    提取处罚机关，根据处罚机关进行数据分类
    :param txt:
    :return:
    """
    data = re.search(r'(落款单位：|特此公告。|视为你放弃听证的权利。|特此公告)(.*)', txt)
    if data:
        return data.group(2)


if __name__ == '__main__':
    # a = get_cf_wsh(aaa)
    # print(a)
    # if '哈' in a:
    #     cf_wsh = 'ffdd'
    # else:
    #     cf_wsh = a
    # print('第二个', cf_wsh)
    txt = '邹少阳（身份证号码：512222196711171614）：本行政机关于2018年6月20日对你做出济历城卫医罚【2018】016号行政处罚决定，已于2018年9月15日公告送达。在法定期限内，你尚未履行该决定，现向你公告送达催告书（济历城卫医催告【2018】020号）。请你自本公告发出起六十日内前来领取催告书，逾期视为送达。如你对此有异议，可在收到本催告书之日起10日内来陈述和申辩，逾期本机关将申请人民法院强制执行。特此公告。联系人：高兆林 电话：0531-83175358 济南市历城区卫生和计划生育局'
    b = get_cf_xzjg(txt=txt)
    print(b)