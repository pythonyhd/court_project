# -*- coding: utf-8 -*-
import pymysql
from DBUtils.PooledDB import PooledDB
import logging
logger = logging.getLogger(__name__)


class MysqlClient(object):

    def __init__(self, host='127.0.0.1', port=3306, user='root', passwd='123456', db='company_name', charset=''):

        self.mysql_pool = PooledDB(creator=pymysql,
                                   host=host,
                                   port=port,
                                   user=user,
                                   passwd=passwd,
                                   db=db,
                                   charset=charset)

    def insert(self, table, item):
        """
        插入item,到mysql制定的表中, 如果插入失败
        :param item: dict类型的数据，并且item中key的名称和mysql一致
        """
        fields = ", ".join(list(item.keys()))
        sub_char = ", ".join(["%s"]*len(item))
        values = tuple(list(item.values()))

        sql = "insert into %s(%s) values (%s)" % (table, fields, sub_char)

        connection = self.mysql_pool.connection()
        cursor = connection .cursor()

        try:
            cursor.execute(sql, values)
            connection .commit()
        except Exception as e:
            if 'Duplicate' in repr(e):
                logger.debug('重复数据')
            else:
                logger.error('errormsg:', e)
            connection .rollback()
        finally:
            cursor.close()
            connection .close()

    def insert_many(self, table, items):
        """
        插入多条数据,利用executemany方法
        :param table: 表名
        :param items: 插入的数据，可迭代对象
        """
        item = items[0]
        fields = ", ".join(list(item.keys()))
        sub_char = ", ".join(["%s"]*len(item))
        value_list = []
        for item in items:
            value = tuple(list(item.values()))
            value_list.append(value)

        sql = "insert into %s(%s) values (%s)" % (table, fields, sub_char)

        # 获取mysql连接和事务
        connection = self.mysql_pool.connection()
        cursor = connection.cursor()

        try:
            cursor.executemany(sql, value_list)
            connection.commit()
            return 1
        except Exception as e:
            connection.rollback()
            raise e
        finally:
            cursor.close()
            connection.close()

    def update_one(self, table, update_item, condition):
        """
        更新表中某个字段
        :param table: mysql 表名
        :param items: dict, 要更新的字段,
        :param condition: dict, 筛选要更新的字段
        :return: None
        """
        fields = ", ".join(['{}="{}"'.format(key, value) for key, value in update_item.items()])
        filter_condition = " and ".join(['{}="{}"'.format(key, value) for key, value in condition.items()])

        sql = "update %s set %s where %s" % (table, fields, filter_condition)

        connection = self.mysql_pool.connection()
        cursor = connection.cursor()

        try:
            cursor.execute(sql)
            connection.commit()
            return 1
        except Exception as e:
            connection.rollback()
            raise e
        finally:
            cursor.close()
            connection.close()

    def update_by_sql(self, sql):
        """
        通过sql语句更新
        """
        connection = self.mysql_pool.connection()
        cursor = connection.cursor()

        try:
            cursor.execute(sql)
            connection.commit()
            return 1
        except Exception as e:
            connection.rollback()
            raise e
        finally:
            cursor.close()
            connection.close()

    def query(self, sql):
        """
        查询
        :param table: 表名
        :param sql: 查询的sql语句
        :return:
        """

        connection = self.mysql_pool.connection()
        cursor = connection.cursor()

        try:
            cursor.execute(sql)
            connection.commit()
            result = cursor.fetchall()
            return result
        except Exception as e:
            raise e
        finally:
            cursor.close()
            connection.close()

    def execute(self, sql):
        """
        执行sql语句,不返回数据
        """
        connection = self.mysql_pool.connection()
        cursor = connection.cursor()

        try:
            cursor.execute(sql)
            connection.commit()
            return 1
        except Exception as e:
            raise e
        finally:
            cursor.close()
            connection.close()


if __name__ == '__main__':
    client = MysqlClient()