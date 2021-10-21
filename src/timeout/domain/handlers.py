import json
import logging

from src.timeout.domain.events import AllSuccess, FirstSuccess, Failed
from src.timeout.domain.model import EventType

logger = logging.getLogger()


def handle_events(message: dict):
    data = json.loads(message["data"])
    if data["event_type"] == EventType.ALL_SUCCESS:
        handle_all_success(data)

    elif data["event_type"] == EventType.FIRST_SUCCESS:
        handle_first_success(data)

    elif data["event_type"] == EventType.FAILED:
        handle_failed(data)


def handle_all_success(data: dict):
    event = AllSuccess(data["event_type"], data["timeout"], data["times"])
    times = " and ".join(event.times)
    logger.info(f"Success for timeout {event.timeout}ms, got {times} ms.")


def handle_first_success(data: dict):
    event = FirstSuccess(data["event_type"], data["timeout"], data["time"])
    logger.info(
        f"Success for timeout {event.timeout}ms, got {event.time} ms."
    )


def handle_failed(data: dict):
    event = Failed(data["event_type"], data["timeout"], data["error"])
    logger.info(
        f"Failure for timeout {event.timeout}ms, got an {event.error}."
    )
