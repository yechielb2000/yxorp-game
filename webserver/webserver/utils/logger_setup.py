from loguru import logger

from webserver.settings import settings

_infra_logger = None
_user_logger = None

INFRA_LOGGER_INDEX = "infra-logs"
USER_LOGGER_INDEX = "user-actions"


def setup_logger():
    global _infra_logger, _user_logger

    logger.remove()

    logger.add(
        settings.user_actions_logs_path,
        rotation="10 MB",
        retention="7 days",
        compression="zip",
        serialize=True,
        level="INFO",
        filter=lambda record: record["extra"].get("index") == USER_LOGGER_INDEX,
        enqueue=True
    )

    logger.add(
        settings.infra_logs_path,
        rotation="10 MB",
        retention="7 days",
        compression="zip",
        serialize=True,
        level="INFO",
        filter=lambda record: record["extra"].get("index") == INFRA_LOGGER_INDEX,
        enqueue=True
    )

    _infra_logger = logger.bind(index=INFRA_LOGGER_INDEX)
    _user_logger = logger.bind(index=USER_LOGGER_INDEX)


def get_infra_logger():
    if not _infra_logger:
        raise ValueError("Infra logger is not initialized yet.")
    return _infra_logger


def get_user_logger():
    if not _user_logger:
        raise ValueError("User logger is not initialized yet.")
    return _user_logger
