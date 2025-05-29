import logging

from elasticsearch import Elasticsearch
from loguru import logger

from webserver.adapters.elastic import get_elasticsearch_client

_infra_logger = None
_user_logger = None


class ElasticSearchLogSink:
    def __init__(self, elastic: Elasticsearch):
        self.elastic = elastic
        self.default_index = "infra-logs"

    def write(self, message):
        """
        In extra, you can pass index value to control what index this log should write to.
        """
        log_doc = {}
        log_record = message.record

        index = message.record["extra"].get("index", self.default_index)

        if index == "infra-logs":
            log_doc = {
                "timestamp": log_record["time"].isoformat(),
                "level": log_record["level"].name,
                "message": log_record["message"],
                "module": log_record["module"],
                "function": log_record["function"],
                "line": log_record["line"],
                "extra": log_record["extra"]
            }
        elif index == "user-actions":
            log_doc = {
                "timestamp": log_record["time"].isoformat(),
                "message": log_record["message"],
                "extra": log_record["extra"]
            }
        self.elastic.index(index=index, document=log_doc)


def setup_logger():
    global _infra_logger, _user_logger

    elastic_client = get_elasticsearch_client()
    es_sink = ElasticSearchLogSink(elastic_client)

    logger.remove()
    logger.add(es_sink, level=logging.INFO)
    _infra_logger = logger.bind(log_type="infra")
    _user_logger = logger.bind(log_type="user-actions")


def get_infra_logger():
    if not _infra_logger:
        raise ValueError("Infra logger is not initialized yet.")
    return _infra_logger


def get_user_logger():
    if not _user_logger:
        raise ValueError("User logger is not initialized yet.")
    return _user_logger
