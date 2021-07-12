# -*- coding: UTF-8 -*-

from elasticsearch import Elasticsearch


class ES():
    def __init__(self):
        self.es = Elasticsearch(['192.168.3.10:9200'])

    #   根据索引，页码获取当页的10个数据
    def match_all(self, index, page):
        page = (int(page) - 1) * 10
        size = 15
        body = {
            "query": {
                "match_all": {}
            },
            "from": page,
            "size": size
        }
        search = self.es.search(index=index, body=body)
        hits_ = search['hits']['hits']
        return hits_

    #   根据索引，id获取指定数据
    def get_id(self, index, id):
        get = self.es.get(index=index, doc_type='doc', id=id)
        # hits_ = get['hits']['hits']
        return get

#   根据索引，条件，页码，精确查找指定数据
    def multi_match(self, index, condition, page):
        page = (int(page) - 1) * 10
        size = 15
        body = {
            "query": {
                "bool": {
                    "must": condition
                }
            },
            "from": page,
            "size": size
        }
        search = self.es.search(index=index, doc_type='doc', body=body)
        hits_ = search['hits']['hits']
        return hits_

