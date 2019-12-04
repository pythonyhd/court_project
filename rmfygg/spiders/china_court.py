# -*- coding: utf-8 -*-
import datetime
import re
from copy import deepcopy
from functools import reduce
from urllib.parse import urljoin

import scrapy

from rmfygg.utils.tests import keyword_generator


class ChinaCourtSpider(scrapy.Spider):
    name = 'china_court_spider'
    allowed_domains = ['chinacourt.org']
    search_url = 'https://www.chinacourt.org/announcement/ggsdsearch'
    custom_settings = {
        'DEFAULT_REQUEST_HEADERS': {
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3",
            "Accept-Encoding": "gzip, deflate, br",
            "Accept-Language": "zh-CN,zh;q=0.9,en-US;q=0.8,en;q=0.7",
            "DNT": "1",
            "Host": "www.chinacourt.org",
            "Pragma": "no-cache",
            "Sec-Fetch-Mode": "navigate",
            "Sec-Fetch-Site": "same-origin",
            "Sec-Fetch-User": "?1",
            "Upgrade-Insecure-Requests": "1",
        },
        "DOWNLOADER_MIDDLEWARES": {
            'rmfygg.middlewares.RandomUserAgentMiddleware': 120,
            'rmfygg.middlewares.MyfreeProxyMiddleware': 150,
            'rmfygg.middlewares.LocalRetryMiddlerware': 180,
        },
        "ITEM_PIPELINES": {
            'rmfygg.pipelines.RmfyggPipeline': 300,
            'rmfygg.pipelines.Save2eEsPipeline': 340,
            # 'rmfygg.pipelines.MysqlTwistedPipeline': 380,
        },
        "SCHEDULER": "scrapy_redis.scheduler.Scheduler",
        "DUPEFILTER_CLASS": "scrapy_redis.dupefilter.RFPDupeFilter",
        "SCHEDULER_QUEUE_CLASS": "scrapy_redis.queue.SpiderPriorityQueue",
        "SCHEDULER_PERSIST": True,
        "REDIRECT_ENABLED": False,
        "RETRY_ENABLED": True,
        "RETRY_TIMES": '9',
        "DOWNLOAD_TIMEOUT": '30',
        # "CONCURRENT_REQUESTS": '16',  # 并发请求(concurrent requests)的最大值，默认16
        # "CONCURRENT_ITEMS": '80',  # 同时处理(每个response的)item的最大值，默认100
        # "CONCURRENT_REQUESTS_PER_DOMAIN": '5',  # 对单个网站进行并发请求的最大值，默认8
        # "DOWNLOAD_DELAY": '0.1',
    }
    base_item = {
        'xxly': '中国法院网-数据补充',
    }

    def start_requests(self):
        """
        搜索入口函数
        :return:
        """
        item = dict()
        results = keyword_generator()
        for kind_id in results:
            if kind_id == '0':
                item['cf_type'] = '公告类型'
                item['cf_zt'] = '公告类型'
                item['cf_cflb'] = '公告类型'
                item['sj_type'] = '77'
                item['site_id'] = 29614
            elif kind_id == '1':
                item['cf_type'] = '起诉状、上诉状副本'
                item['cf_zt'] = '起诉状、上诉状副本'
                item['cf_cflb'] = '起诉状、上诉状副本'
                item['sj_type'] = '77'
                item['site_id'] = 29614
            elif kind_id == '2':
                item['cf_type'] = '开庭传票'
                item['cf_zt'] = '开庭传票'
                item['cf_cflb'] = '开庭传票'
                item['sj_type'] = '75'
                item['site_id'] = 29035
            elif kind_id == '3':
                item['cf_type'] = '裁判文书'
                item['cf_zt'] = '裁判文书'
                item['cf_cflb'] = '裁判文书'
                item['sj_type'] = '74'
                item['site_id'] = 29206
            elif kind_id == '4':
                item['cf_type'] = '公示催告'
                item['cf_zt'] = '公示催告'
                item['cf_cflb'] = '公示催告'
                item['sj_type'] = '77'
                item['site_id'] = 29614
            elif kind_id == '5':
                item['cf_type'] = '破产文书'
                item['cf_zt'] = '破产文书'
                item['cf_cflb'] = '破产文书'
                item['sj_type'] = '77'
                item['site_id'] = 29614
            elif kind_id == '6':
                item['cf_type'] = '宣告失踪、死亡'
                item['cf_zt'] = '宣告失踪、死亡'
                item['cf_cflb'] = '宣告失踪、死亡'
                item['sj_type'] = '77'
                item['site_id'] = 29614
            elif kind_id == '7':
                item['cf_type'] = '执行文书'
                item['cf_zt'] = '执行文书'
                item['cf_cflb'] = '执行文书'
                item['sj_type'] = '76'
                item['site_id'] = 29236
            elif kind_id == '8':
                item['cf_type'] = '无主财产认领公告'
                item['cf_zt'] = '无主财产认领公告'
                item['cf_cflb'] = '无主财产认领公告'
                item['sj_type'] = '77'
                item['site_id'] = 29614
            elif kind_id == '9':
                item['cf_type'] = '起诉状副本及开庭传票'
                item['cf_zt'] = '起诉状副本及开庭传票'
                item['cf_cflb'] = '起诉状副本及开庭传票'
                item['sj_type'] = '77'
                item['site_id'] = 29614
            elif kind_id == '10':
                item['cf_type'] = '其他'
                item['cf_zt'] = '其他'
                item['cf_cflb'] = '其他'
                item['sj_type'] = '77'
                item['site_id'] = 29614
            elif kind_id == '11':
                item['cf_type'] = '更正'
                item['cf_zt'] = '更正'
                item['cf_cflb'] = '更正'
                item['sj_type'] = '77'
                item['site_id'] = 29614
            elif kind_id == '12':
                item['cf_type'] = '遗失声明'
                item['cf_zt'] = '遗失声明'
                item['cf_cflb'] = '遗失声明'
                item['sj_type'] = '77'
                item['site_id'] = 29614
            elif kind_id == '13':
                item['cf_type'] = '司法鉴定书'
                item['cf_zt'] = '司法鉴定书'
                item['cf_cflb'] = '司法鉴定书'
                item['sj_type'] = '77'
                item['site_id'] = 29614
            elif kind_id == '14':
                item['cf_type'] = '海事文书'
                item['cf_zt'] = '海事文书'
                item['cf_cflb'] = '海事文书'
                item['sj_type'] = '77'
                item['site_id'] = 29614
            elif kind_id == '15':
                item['cf_type'] = '仲裁文书'
                item['cf_zt'] = '仲裁文书'
                item['cf_cflb'] = '仲裁文书'
                item['sj_type'] = '20'
                item['site_id'] = 29583
            elif kind_id == '16':
                item['cf_type'] = '拍卖公告'
                item['cf_zt'] = '拍卖公告'
                item['cf_cflb'] = '拍卖公告'
                item['sj_type'] = '17'
                item['site_id'] = 29568
            elif kind_id == '17':
                item['cf_type'] = '清算公告'
                item['cf_zt'] = '清算公告'
                item['cf_cflb'] = '清算公告'
                item['sj_type'] = '77'
                item['site_id'] = 29614
            elif kind_id == '18':
                item['cf_type'] = '行政处罚通知书'
                item['cf_zt'] = '行政处罚通知书'
                item['cf_cflb'] = '行政处罚通知书'
                item['sj_type'] = '54'
                item['site_id'] = 29651
            elif kind_id == '19':
                item['cf_type'] = '版权公告'
                item['cf_zt'] = '版权公告'
                item['cf_cflb'] = '版权公告'
                item['sj_type'] = '77'
                item['site_id'] = 29614
            elif kind_id == '20':
                item['cf_type'] = '公益诉讼'
                item['cf_zt'] = '公益诉讼'
                item['cf_cflb'] = '公益诉讼'
                item['sj_type'] = '77'
                item['site_id'] = 29614
            form_data = {
                'kind_id': kind_id,
                'content_announcer': '',
                'content_party': '',
                'publishdate1': '2016-05-16',
                'publishdate2': str(datetime.datetime.now().strftime("%Y-%m-%d")),
                'content_main': '',
                'page': '1',
            }

            yield scrapy.FormRequest(
                url=self.search_url,
                formdata=form_data,
                method='GET',
                meta={'base_item': deepcopy(item)}
            )

    def parse(self, response):
        """
        解析响应数据
        :param response: 列表HTML
        :return: 请求详情
        """
        base_item = response.meta.get('base_item')
        # 解析
        selector = scrapy.Selector(text=response.text)
        base_dom = selector.xpath('//div[@class="list_content"]/table/tr[position() > 1]')
        for data in base_dom:
            xq_url = data.xpath('.//a/@href').get()
            court_name = data.xpath('./td[1]/a/text()').get('')
            oname = data.xpath('./td[2]/a/text()').get('')
            fb_rq = data.xpath('./td[3]/text()').get('')
            link = urljoin(response.url, xq_url)
            meta_data = {'oname': oname, 'cf_xzjg': court_name, 'fb_rq': fb_rq}
            meta_data = {**meta_data, **base_item}
            # 详情
            yield scrapy.Request(
                url=link,
                callback=self.parse_detail,
                meta={'item': meta_data},
                priority=5,
            )

        # 列表翻页
        next_num = selector.xpath('//a[contains(., "尾页")]/@href').get()
        if next_num:
            next_num = re.search(r'page/(\d+)\.shtml', next_num).group(1)
            is_first = response.meta.get('is_first', True)
            if int(next_num) > 50:
                page_num = 50
            else:
                page_num = next_num
            if is_first:
                for page in range(2, int(page_num) + 1):
                    link = response.url.replace('page=1', 'page={}'.format(str(page)))
                    yield scrapy.Request(
                        url=link,
                        meta={'is_first': False, 'base_item': base_item},
                        priority=3,
                    )

    def parse_detail(self, response):
        """
        详情页解析
        :param response: 详情HTML
        :return: item
        """
        item = response.meta.get('item')
        re_com = re.compile(r'\r|\n|\t|\s')
        selector = scrapy.Selector(text=response.text)
        ws_content = selector.xpath('//div[@class="ggcx"]//text()').getall()
        ws_nr_txt = reduce(lambda x, y: x + y, [re_com.sub('', i) for i in ws_content])
        item['xq_url'] = response.url
        item['ws_nr_txt'] = ws_nr_txt
        item['cf_jg'] = ws_nr_txt
        court_item = {**item, **self.base_item}
        # print(court_item)
        yield court_item
