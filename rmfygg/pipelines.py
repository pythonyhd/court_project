# -*- coding: utf-8 -*-
import re
import json
import time
import math

import redis
from scrapy.exceptions import DropItem
import pymysql
from twisted.enterprise import adbapi
import logging

from rmfygg import settings
from rmfygg.utils.elastic_common import EsObject
from rmfygg.work_utils.court_filter import filter_factory

logger = logging.getLogger(__name__)


class RmfyggPipeline(object):
    """
    数据简单清洗
    """
    def __deal_with_data(self, txt):
        data = re.sub(r'[\r\n\t\s&ensp;</br></br>]', '', txt)
        return data

    @classmethod
    def _get_cf_wsh(cls, txt):
        """
        文书号匹配规则
        """
        if txt:
            data = re.search(r'([\[\(（]\d{4}.*?号)', txt)
            if data:
                data = data.group()
            else:
                data = ''
            return data
        else:
            return ''

    @classmethod
    def _get_zqr(cls, txt):
        if txt:
            data = re.search(r'(原告|原告为|上诉人|执行人)(.*?)(诉|与|申请宣告)', txt)
            if data:
                return data.group(2)
            else:
                return ''
        else:
            return ''

    @classmethod
    def _get_cf_sy(cls, txt):
        if txt:
            data = re.search(r'(.*?一案)', txt)
            if data:
                return data.group(1)
            else:
                return ''
        else:
            return ''

    def process_item(self, item, spider):
        item['cj_sj'] = math.ceil(time.time())
        # item['cj_sj'] = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))
        item['sj_ztxx'] = 1
        item['cf_jg'] = self.__deal_with_data(item.get('cf_jg'))
        item['ws_nr_txt'] = self.__deal_with_data(item.get('ws_nr_txt'))
        item['cf_wsh'] = self._get_cf_wsh(item['ws_nr_txt'])
        item['zqr'] = self._get_zqr(item['ws_nr_txt'])
        item['cf_sy'] = self._get_cf_sy(item['ws_nr_txt'])
        ws_pc_id = filter_factory(item)
        if ws_pc_id:
            item['ws_pc_id'] = ws_pc_id
        else:
            DropItem(item)
        # print(item)
        return item


class MysqlTwistedPipeline(object):
    """
    mysql异步存储
    """

    def __init__(self, dbpool):
        self.dbpool = dbpool
        self.table_name = 'axy_data'
        self.redis_client = redis.StrictRedis(
            host=settings.REDIS_HOST,
            port=settings.REDIS_PORT,
            password=settings.REDIS_PASSWORD,
            db=settings.REDIS_DB,
        )

    @classmethod
    def from_settings(cls, settings):
        dbparms = dict(
            host=settings["DB_HOST"],
            db=settings["DB_NAME"],
            user=settings["DB_USER"],
            passwd=settings["DB_PASSWORD"],
            charset=settings["DB_CHARSET"],
            cursorclass=pymysql.cursors.DictCursor,
            use_unicode=True,
        )
        dbpool = adbapi.ConnectionPool('pymysql', **dbparms)  # 连接
        return cls(dbpool)

    def process_item(self, item, spider):
        query = self.dbpool.runInteraction(self.do_insert, item)  # 调用twisted进行异步的插入操作
        query.addErrback(self.handle_error, item, spider)

    def do_insert(self, cursor, item):
        fields = ", ".join(list(item.keys()))
        sub_char = ", ".join(["%s"]*len(item))
        values = tuple(list(item.values()))
        sql = "insert into %s(%s) values (%s)" % (self.table_name, fields, sub_char)
        try:
            cursor.execute(sql, values)
        except Exception as e:
            if "Duplicate" in repr(e):
                logger.debug("数据重复，跳过")
                DropItem(item)
            else:
                logger.debug('插入失败,errormsg:{}'.format(repr(e)))
                self.redis_client.sadd("court:insert_err_items", json.dumps(dict(item), ensure_ascii=False))

    def handle_error(self, failure, item, spider):
        logger.error("插入失败原因:{}".format(failure))


class Save2eEsPipeline(object):
    def __init__(self):
        self.es = EsObject(index_name=settings.INDEX_NAME, index_type=settings.INDEX_TYPE, host=settings.ES_HOST, port=settings.ES_PORT)

    def process_item(self, item, spider):
        if item:
            # 获取唯一ID
            _id = item['ws_pc_id']
            res1 = self.es.get_data_by_id(_id)
            if res1.get('found') == True:
                logger.debug("该数据已存在%s" % _id)
            else:
                self.es.insert_data(dict(item), _id)
                logger.debug("----------抓取成功,开始插入数据%s" % _id)
                return item


class RedisPipeline(object):
    """
    法院名称放到服务器redis
    """
    def __init__(self, redis_host, redis_port, redis_db, redis_password):
        self.pool = redis.ConnectionPool(host=redis_host, port=redis_port, db=redis_db, password=redis_password)
        self.client = redis.Redis(connection_pool=self.pool, decode_responses=True)

    @classmethod
    def from_crawler(cls, crawler):
        return cls(
            redis_host=crawler.settings.get('REDIS_HOST'),
            redis_port=crawler.settings.get('REDIS_PORT'),
            redis_db=crawler.settings.get('REDIS_DB'),
            redis_password=crawler.settings.get('REDIS_PASSWORD'),
        )

    def close_spider(self, spider):
        self.client.close()

    def process_item(self, item, spider):
        self.insert_item(item)
        return item

    def insert_item(self, item):
        if isinstance(item, dict):
            results = item.get('name')
            self.client.sadd('court:name', results)
            # print(results)
            # for i in results:
                # self.client.rpush('court:name', i)  # 存list
                # self.client.sadd('court:name', i)  # 存集合，去重

