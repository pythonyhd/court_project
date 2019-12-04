# -*- coding: utf-8 -*-
from scrapy.cmdline import execute


# execute("scrapy crawl rmfy_court_update".split())  # 人民法院公告网-日常更新-每天50页
# execute("scrapy crawl court".split())  # 人民法院公告网-法院名称搜索-抓全站-不需要部署
execute("scrapy crawl china_court_spider".split())  # 中国法院网-法院公告-周更2次