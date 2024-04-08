from functools import lru_cache

from elasticsearch import AuthenticationException

from recom_system.settings import ELASTICSEARCH_CONNECTION, ES_INDEX_PREFIX


class ElasticSearchStorage:
    _instance = None

    def __init__(self, index_prefix):
        self.es = ELASTICSEARCH_CONNECTION
        self.index_prefix = index_prefix

    def get_index_name(self, res_id):
        return f"{self.index_prefix}_{res_id}"

    def store_similarity(self, res_id, doc):
        self.es.index(index=self.get_index_name(res_id), body=doc)

    def get_similarities_by_res_id(self, res_id, user_name):
        result = self.es.search(index=self.get_index_name(res_id))
        return [hit['_source'] for hit in result['hits']['hits'] if
                hit['_source']['user_name'] == user_name]

    def clear(self):
        self.es.indices.delete(index='_all')

    @classmethod
    def build(cls):
        if cls._instance is None:
            cls._instance = cls(index_prefix=ES_INDEX_PREFIX)
        return cls._instance

    @classmethod
    @lru_cache(maxsize=None)
    def get_instance(cls):
        if cls._instance is None:
            cls._instance = cls.build()
        return cls._instance
