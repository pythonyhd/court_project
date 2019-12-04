# -*- coding: utf-8 -*-
import datetime

BOT_NAME = 'rmfygg'

SPIDER_MODULES = ['rmfygg.spiders']
NEWSPIDER_MODULE = 'rmfygg.spiders'

"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
scrapy基本配置
"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
ROBOTSTXT_OBEY = False
# LOG_LEVEL = 'INFO'


"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
数据存储到数据库
"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
# --------------存储到elasticsearch-----------------#
ES_HOST = '49.4.22.216'
ES_PORT = 9999
ES_USERNAME = ''
ES_PASSWORD = ''
INDEX_NAME = 'cf_index_db'
INDEX_TYPE = 'xzcf'

# --------------存储到mysql-----------------#
today = datetime.datetime.today()
year = today.year
month = today.month
# DB_HOST = "49.4.86.151"
DB_HOST = "192.168.1.54"
DB_PORT = 3306
DB_USER = 'root'
# DB_PASSWORD = 'mysql@Axinyong123'
DB_PASSWORD = 'root'
# DB_PASSWORD = '123456'
DB_NAME = 'axy_data_db_{}'.format(str(year)[2:4]+str(month))
DB_CHARSET = 'utf8'

"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
redis 相关配置
"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
# 存储连接配置
# REDIS_HOST = '127.0.0.1'
REDIS_HOST = '114.115.201.98'
REDIS_PORT = 6379
REDIS_PASSWORD = 'axy@2019'
REDIS_DB = 3
REDIS_PARAMS = {
    "password": "axy@2019",
    "db": 3,
}

# 代理连接配置
# REDIS_PROXIES_HOST = '192.168.1.30'
REDIS_PROXIES_HOST = '117.78.35.12'
REDIS_PROXIES_PORT = 6379
REDIS_PROXIES_PASSWORD = ''
REDIS_PROXIES_DB = 15

"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
scrapy请求头
"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
RANDOM_UA_TYPE = "random"