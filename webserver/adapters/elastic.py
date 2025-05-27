from elasticsearch import Elasticsearch

from webserver.settings import Settings


def get_elasticsearch_client():
    return Elasticsearch(Settings.elasticsearch_url)
