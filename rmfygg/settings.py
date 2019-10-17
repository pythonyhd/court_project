# -*- coding: utf-8 -*-
import datetime

BOT_NAME = 'rmfygg'

SPIDER_MODULES = ['rmfygg.spiders']
NEWSPIDER_MODULE = 'rmfygg.spiders'

# --------------scrapy-爬取 设置-----------------#
ROBOTSTXT_OBEY = False
CONCURRENT_REQUESTS = 20
# DOWNLOAD_DELAY = 1
RETRY_ENABLED = True
RETRY_TIMES = 9  # 重试次数
REDIRECT_ENABLED = False  # 禁止重定向,默认是True
DOWNLOAD_TIMEOUT = 20  # 下载超时时间默认180
# REACTOR_THREADPOOL_MAXSIZE = 20  # 增加处理DNS查询的线程数
# COOKIES_ENABLED = True
LOG_LEVEL = 'INFO'
RANDOM_UA_TYPE = 'random'
SPIDER_ERRROR_URLS = 'rmfygg:crawl_error_urls'
# COMPRESSION_ENABLED = False
# 调度去重等等
SCHEDULER = "scrapy_redis.scheduler.Scheduler"
DUPEFILTER_CLASS = "scrapy_redis.dupefilter.RFPDupeFilter"
SCHEDULER_QUEUE_CLASS = 'scrapy_redis.queue.SpiderPriorityQueue'
SCHEDULER_PERSIST = True

DOWNLOADER_MIDDLEWARES = {
   'scrapy.downloadermiddlewares.retry.RetryMiddleware': None,
   'rmfygg.middlewares.RandomUserAgentMiddleware': 150,
   'scrapy.downloadermiddlewares.httpproxy.HttpProxyMiddleware': None,  # 禁用默认的代理
   'rmfygg.middlewares.MyfreeProxyMiddleware': 180,
   'rmfygg.middlewares.LocalRetryMiddlerware': 280,
}


ITEM_PIPELINES = {
   'rmfygg.pipelines.RmfyggPipeline': 350,
   'rmfygg.pipelines.MysqlTwistedPipeline': 400,
   # 'rmfygg.pipelines.RedisPipeline': 400,
}

# --------------scrapy-存储到mongodb设置-----------------#
MONGO_URI = '127.0.0.1'
MONGO_DATA_BASE = 'db_court'

# --------------scrapy-存储到mysql设置-----------------#
today = datetime.datetime.today()
year = today.year
month = today.month
# DB_HOST = "49.4.86.151"
DB_HOST = "127.0.0.1"
DB_PORT = 3306
DB_USER = 'root'
# DB_PASSWORD = 'mysql@Axinyong123'
# DB_PASSWORD = 'root'
DB_PASSWORD = '123456'
DB_NAME = 'axy_data_db_{}'.format(str(year)[2:4]+str(month))
DB_CHARSET = 'utf8'


# --------------redis连接配置-----------------#
# 代理连接配置
REDIS_PROXIES_HOST = '117.78.35.12'
REDIS_PROXIES_PORT = 6379
REDIS_PROXIES_PASSWORD = ''
REDIS_PROXIES_DB = 15
# 存储连接配置
# REDIS_HOST = '127.0.0.1'
REDIS_HOST = '114.115.201.98'
REDIS_PORT = 6379
REDIS_PASSWORD = 'axy@2019'
REDIS_DB = 3
# 指定 redis链接密码，和使用哪一个数据库,可以在scrapy_redis里面的defults文件查看
REDIS_PARAMS = {
    "password": "axy@2019",
    "db": 3,
}