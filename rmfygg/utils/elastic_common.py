# -*- coding: utf-8 -*-
from elasticsearch import Elasticsearch


class EsObject:

    def __init__(self, index_name, index_type, host, port):
        self.index_name = index_name
        self.index_type = index_type
        self.es = Elasticsearch([{'host': host, 'port': port}], timeout=3600)

    def insert_data(self, item, _id):
        result = self.es.create(index=self.index_name, doc_type=self.index_type, id=_id, body=item)
        return result

    def update_data(self, item, _id):
        result = self.es.update(index=self.index_name, doc_type=self.index_type, id=_id, body=item)
        return result

    def get_data_by_id(self, _id):
        result = self.es.get(index=self.index_name, doc_type=self.index_type, id=_id, ignore=[404])
        return result


if __name__ == '__main__':
    data1 = {
        "title": "爱我中华",
        "test1": 123,
        "test2": None
    }
    test_es = EsObject(index_name='cf_index_db', index_type='xzcf')
    res = test_es.get_data_by_id("102")
    print(res['found'])
    print(res)