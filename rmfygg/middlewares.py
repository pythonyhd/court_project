# -*- coding: utf-8 -*-
from fake_useragent import UserAgent
import redis
import random
import base64
from scrapy.downloadermiddlewares.retry import RetryMiddleware
from scrapy.exceptions import IgnoreRequest
from scrapy.utils.python import global_object_name
from scrapy.utils.response import response_status_message
from rmfygg import settings
import logging
logger = logging.getLogger(__name__)


class RandomUserAgentMiddleware(object):
    """
    随机请求头
    """
    def __init__(self, ua_type):
        self.ua_type = ua_type
        self.ua = UserAgent()

    @classmethod
    def from_crawler(cls, crawler):
        return cls(
            ua_type=crawler.settings.get('RANDOM_UA_TYPE', 'random'),
        )

    def process_request(self, request, spider):
        def get_user_agent():
            return getattr(self.ua, self.ua_type)
        request.headers.setdefault(b'User-Agent', get_user_agent())


class MyfreeProxyMiddleware(object):
    def __init__(self, proxy_redis_host, proxy_redis_port, proxy_redis_password, proxy_redis_db):
        self.redis = redis.StrictRedis(host=proxy_redis_host, port=proxy_redis_port, password=proxy_redis_password, db=proxy_redis_db)

    @classmethod
    def from_crawler(cls, crawler):
        return cls(
            proxy_redis_host=crawler.settings.get('REDIS_PROXIES_HOST'),
            proxy_redis_port=crawler.settings.get('REDIS_PROXIES_PORT'),
            proxy_redis_password=crawler.settings.get('REDIS_PROXIES_PASSWORD'),
            proxy_redis_db=crawler.settings.get('REDIS_PROXIES_DB'),
        )

    def delete_proxy(self, proxy):
        """
        删除代理
        """
        self.redis.srem("proxies", proxy)

    def delete_free_proxy(self, proxy):
        """
        删除免费代理
        :param proxy:
        :return:
        """
        self.redis.zrem('freeproxies', proxy)

    def process_request(self, request, spider):
        # free_proxies = self.redis.zrevrange('freeproxies', 0, 100)
        ip_port = self.redis.srandmember('proxies')
        # proxies = {
        #     'http:': 'http://{}'.format(random.choice(free_proxies).decode('utf-8')),
        #     'https:': 'https://{}'.format(random.choice(free_proxies).decode('utf-8')),
        # }
        proxies = {
            'http:': 'http://{}'.format(ip_port.decode('utf-8')),
            'https:': 'https://{}'.format(ip_port.decode('utf-8')),
        }
        if request.url.startswith('http://'):
            request.meta['proxy'] = proxies.get("http:")
            logger.debug('http链接,ip:{}'.format(request.meta.get('proxy')))
        else:
            request.meta['proxy'] = proxies.get('https:')
            logger.debug('https链接,ip:{}'.format(request.meta.get('proxy')))

    def process_response(self, request, response, spider):
        if response.status in [300, 301, 302]:
            try:
                redirect_url = response.headers.get('location')
                logger.error('出现重定向，需要处理，url:{}'.format(redirect_url))
                if 'login' in redirect_url:
                    logger.info('需要登录')
                return request
            except:
                raise IgnoreRequest

        elif response.status in [414, 500, 503, 533, 564, 562]:
            return request

        elif response.status == 403:
            proxy_spider = request.meta.get('proxy')
            proxy_redis = proxy_spider.split("//")[1]
            self.delete_proxy(proxy_redis)
            return request

        else:
            return response

    def process_exception(self, request, exception, spider):
        # print(repr(exception))
        if 'ConnectionRefusedError' in repr(exception):
            proxy = request.meta.get('proxy')
            if proxy:
                proxy = proxy.split("//")[1]
                # self.delete_free_proxy(proxy)
                self.delete_proxy(proxy)
                logger.info('目标计算机积极拒绝，删除代理-{}-请求url-{}-重新请求'.format(proxy, request.url))
                return request
            else:
                logger.info('无代理')

        elif 'TCPTimedOutError' in repr(exception):
            proxy = request.meta.get('proxy')
            if proxy:
                proxy = proxy.split("//")[1]
                # self.delete_free_proxy(proxy)
                self.delete_proxy(proxy)
                logger.info('连接方在一段时间后没有正确答复或连接的主机没有反应，删除代理-{}-请求url-{}-重新请求'.format(proxy, request.url))
                return request
            else:
                logger.info('无代理')

        elif 'TimeoutError' in repr(exception):
            logger.info('请求超时-请求url-{}-重新请求'.format(request.url))
            return request

        else:
            logger.error('出现其他异常:{}--等待处理'.format(repr(exception)))


class LocalRetryMiddlerware(RetryMiddleware):
    """
    重新定义重试中间件
    """
    redis_client = redis.StrictRedis(
        host=settings.REDIS_HOST,
        port=settings.REDIS_PORT,
        password=settings.REDIS_PASSWORD,
        db=settings.REDIS_DB,
    )

    def process_response(self, request, response, spider):

        if request.meta.get('dont_retry', False):
            return response
        if response.status in self.retry_http_codes:
            reason = response_status_message(response.status)
            return self._retry(request, reason, spider) or response
        return response

    def _retry(self, request, reason, spider):
        retries = request.meta.get('retry_times', 0) + 1

        retry_times = self.max_retry_times

        if 'max_retry_times' in request.meta:
            retry_times = request.meta['max_retry_times']

        stats = spider.crawler.stats
        if retries <= retry_times:
            logger.debug("Retrying %(request)s (failed %(retries)d times): %(reason)s",
                         {'request': request, 'retries': retries, 'reason': reason},
                         extra={'spider': spider})
            retryreq = request.copy()
            retryreq.meta['retry_times'] = retries
            retryreq.dont_filter = True
            retryreq.priority = request.priority + self.priority_adjust

            if isinstance(reason, Exception):
                reason = global_object_name(reason.__class__)

            stats.inc_value('retry/count')
            stats.inc_value('retry/reason_count/%s' % reason)
            return retryreq
        else:
            # 全部重试错误，要保存错误的url和参数 - start
            error_request = settings.SPIDER_ERRROR_URLS
            self.redis_client.sadd(error_request, request.url)
            # 全部重试错误，要保存错误的url和参数 - en
            stats.inc_value('retry/max_reached')
            logger.debug("Gave up retrying %(request)s (failed %(retries)d times): %(reason)s",
                         {'request': request, 'retries': retries, 'reason': reason},
                         extra={'spider': spider})
