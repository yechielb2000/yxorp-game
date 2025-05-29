from elasticsearch import Elasticsearch

from webserver.settings import settings


def get_elasticsearch_client():
    return Elasticsearch(settings.elasticsearch_url)
