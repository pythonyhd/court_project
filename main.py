# -*- coding: utf-8 -*-
from scrapy.cmdline import execute
import sys, os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))


# execute("scrapy crawl court_update".split())  # 人民法院公告网-日常更新-每天50页
execute("scrapy crawl court".split())  # 人民法院公告网-两个搜索条件抓取