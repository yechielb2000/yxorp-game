import os

from elasticsearch import Elasticsearch

ELASTICSEARCH_URL = os.getenv("ELASTICSEARCH_URL")


def get_elasticsearch_client():
    return Elasticsearch(ELASTICSEARCH_URL)
