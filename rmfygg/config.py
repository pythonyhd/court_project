# -*- coding: utf-8 -*-


court_custom_settings = {
        "DEFAULT_REQUEST_HEADERS": {
            "accept": "application/json, text/javascript, */*; q=0.01",
            "accept-encoding": "gzip, deflate, br",
            "accept-language": "zh-CN,zh;q=0.9,en-US;q=0.8,en;q=0.7",
            "content-type": "application/x-www-form-urlencoded; charset=UTF-8",
            "x-requested-with": "XMLHttpRequest",
            "origin": "https://rmfygg.court.gov.cn",
            "referer": "https://rmfygg.court.gov.cn/web/rmfyportal/noticeinfo",
        },
        "DOWNLOADER_MIDDLEWARES": {
            'rmfygg.middlewares.RandomUserAgentMiddleware': 150,
            'scrapy.downloadermiddlewares.httpproxy.HttpProxyMiddleware': None,  # 禁用默认的代理
            'rmfygg.middlewares.MyfreeProxyMiddleware': 180,
            'scrapy.downloadermiddlewares.retry.RetryMiddleware': None,
            'rmfygg.middlewares.LocalRetryMiddlerware': 280,
        },
        "ITEM_PIPELINES": {
            'rmfygg.pipelines.RmfyggPipeline': 350,
            # 'rmfygg.pipelines.Save2eEsPipeline': 370,
            'rmfygg.pipelines.MongodbIndexPipeline': 370,
            # 'rmfygg.pipelines.MysqlTwistedPipeline': 400,
        },
        "SCHEDULER": "scrapy_redis.scheduler.Scheduler",
        "DUPEFILTER_CLASS": "scrapy_redis.dupefilter.RFPDupeFilter",
        "SCHEDULER_QUEUE_CLASS": "scrapy_redis.queue.SpiderPriorityQueue",
        "SCHEDULER_PERSIST": True,
        "REDIRECT_ENABLED": False,
        'COOKIES_ENABLED': False,
        "RETRY_ENABLED": True,
        "RETRY_TIMES": '9',
        "DOWNLOAD_TIMEOUT": '30',
        # "CONCURRENT_REQUESTS": '16',  # 并发请求(concurrent requests)的最大值，默认16
        # "CONCURRENT_ITEMS": '80',  # 同时处理(每个response的)item的最大值，默认100
        # "CONCURRENT_REQUESTS_PER_DOMAIN": '5',  # 对单个网站进行并发请求的最大值，默认8
        # "DOWNLOAD_DELAY": '0.1',
    }


china_court_settings = {
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