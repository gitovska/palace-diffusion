from logging import INFO, WARNING, Logger, basicConfig, getLogger


def create_logger() -> Logger:
    basicConfig(
        format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=INFO
    )
    getLogger("httpx").setLevel(WARNING)
    return getLogger(__name__)


LOGGER = create_logger()
