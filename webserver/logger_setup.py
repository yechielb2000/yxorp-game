import logging

from elasticsearch import Elasticsearch
from loguru import logger

from webserver.adapters.elastic import get_elasticsearch_client


class ElasticSearchLogSink:
    def __init__(self, elastic: Elasticsearch):
        self.elastic = elastic
        self.default_index = "infra-logs"

    def write(self, message):
        """
        In extra, you can pass index value to control what index this log should write to.
        """
        log_record = message.record

        index = message.record["extra"].get("index", self.default_index)

        log_doc = {
            "timestamp": log_record["time"].isoformat(),
            "level": log_record["level"].name,
            "message": log_record["message"],
            "module": log_record["module"],
            "function": log_record["function"],
            "line": log_record["line"],
        }

        self.elastic.index(index=index, document=log_doc)


def setup_logger():
    elastic_client = get_elasticsearch_client()
    es_sink = ElasticSearchLogSink(elastic_client)
    # logger.remove()
    logger.add(es_sink, level=logging.INFO)
