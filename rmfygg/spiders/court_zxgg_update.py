# -*- coding: utf-8 -*-
import scrapy
import json
import re
from copy import deepcopy


class CourtZxggUpdateSpider(scrapy.Spider):
    name = 'court_zxgg_update'
    post_url = 'https://rmfygg.court.gov.cn/web/rmfyportal/noticeinfo?p_p_id=noticelist_WAR_rmfynoticeListportlet&p_p_lifecycle=2&p_p_state=normal&p_p_mode=view&p_p_resource_id=initNoticeList&p_p_cacheability=cacheLevelPage&p_p_col_id=column-1&p_p_col_count=1'

    def start_requests(self):
        """
        每天更新，只能翻50页
        :return:
        """
        for page in range(1, 51):
            handle_list = [
                {"name": "sEcho", "value": page},
                {"name": "iColumns", "value": 6},
                {"name": "sColumns", "value": ",,,,,"},
                {"name": "iDisplayStart", "value": 15 * (page - 1)},
                {"name": "iDisplayLength", "value": 15},
                {"name": "mDataProp_0", "value": "null"},
                {"name": "mDataProp_1", "value": "null"},
                {"name": "mDataProp_2", "value": "null"},
                {"name": "mDataProp_3", "value": "null"},
                {"name": "mDataProp_4", "value": "null"},
                {"name": "mDataProp_5", "value": "null"}
            ]
            form_data = {
                '_noticelist_WAR_rmfynoticeListportlet_content': '',
                '_noticelist_WAR_rmfynoticeListportlet_searchContent': '',
                '_noticelist_WAR_rmfynoticeListportlet_courtParam': '',
                '_noticelist_WAR_rmfynoticeListportlet_IEVersion': 'ie',
                '_noticelist_WAR_rmfynoticeListportlet_flag': 'click',
                '_noticelist_WAR_rmfynoticeListportlet_noticeTypeVal': '执行文书',
                '_noticelist_WAR_rmfynoticeListportlet_aoData': str(handle_list),
            }
            yield scrapy.FormRequest(
                url=self.post_url,
                formdata=form_data,
                callback=self.parse_index,
            )

    def parse_index(self, response):
        item = {}
        results = json.loads(response.text)
        data_list = results.get('data')
        for data in data_list:
            cf_xzjg = data.get('court')  # 列表页法院名称
            # item['name'] = cf_xzjg
            # yield item
            item['cf_xzjg'] = cf_xzjg
            # noticeCode = data.get('noticeCode')  # pdf得位置
            # noticeCodeEnc = data.get('noticeCodeEnc')  # pdf下载参数
            item['ws_nr_txt'] = data.get('noticeContent')  # 内容
            item['cf_cflb'] = data.get('noticeType')  # 类型
            # tosendPeople = data.get('tosendPeople')  # 当事人
            item['fb_rq'] = data.get('publishDate')  # 发布日期
            uuid = data.get('uuid')  # 详情页参数
            item['xq_url'] = 'https://rmfygg.court.gov.cn/web/rmfyportal/noticedetail?paramStr={}'.format(uuid)
            form_data = {"_noticedetail_WAR_rmfynoticeDetailportlet_uuid": str(uuid)}
            url = 'https://rmfygg.court.gov.cn/web/rmfyportal/noticedetail?p_p_id=noticedetail_WAR_rmfynoticeDetailportlet&p_p_lifecycle=2&p_p_state=normal&p_p_mode=view&p_p_resource_id=noticeDetail&p_p_cacheability=cacheLevelPage&p_p_col_id=column-1&p_p_col_count=1'
            yield scrapy.FormRequest(
                url=url,
                formdata=form_data,
                priority=2,
                callback=self.parse_index_page,
                meta={'item': deepcopy(item)},
            )

    def parse_index_page(self, response):
        item = response.meta.get('item')
        results = json.loads(response.text)
        item['sf_sl'] = results.get('court')  # 法院名称
        item['cf_jg'] = results.get('noticeContent')  # 文书内容
        item['cf_type'] = results.get('noticeType')  # 文书类型
        item['sf'] = results.get('province')  # 省份
        item['cf_jdrq'] = results.get('publishDate')  # 决定日期
        item['bz'] = results.get('publishPage')  # 刊登版面
        item['cf_zt'] = '执行文书'
        item['cf_cfmc'] = results.get('tosendPeople')  # 当事人
        if item['cf_cfmc']:
            item['oname'] = item['cf_cfmc']
        else:
            item['oname'] = get_oname(item['cf_jg'])
        item['zqr'] = get_zqr(item['cf_jg'])
        item['cf_sy'] = get_cf_sy(item['cf_jg'])
        item['cf_wsh'] = get_cf_wsh(item['cf_jg'])
        item['sj_type'] = 76
        item['xxly'] = '人民法院公告网-执行公告'
        item['site_id'] = 29236
        item['sj_ztxx'] = 1
        yield item


def get_oname(txt):
    """
    获取被告
    :param txt:
    :return:
    """
    if txt:
        data = re.search(r'(被告|被告人)(.*?公司)', txt)
        if data:
            return data.group(2)
        else:
            return ""
    else:
        return ""


def get_zqr(txt):
    """
    提取原告
    :param txt:
    :return:
    """
    if txt:
        data = re.search(r'(原告|上诉人|申请人)(.*?)(诉|与)', txt)
        if data:
            return data.group(2)
        else:
            return ""
    else:
        return ""


def get_cf_sy(txt):
    """
    提取事由
    :param txt:
    :return:
    """
    if txt:
        data = re.search(r'(.*?一案)', txt)
        if data:
            return data.group(1)
        else:
            return ""
    else:
        return ""


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
            return ""
    else:
        return ""