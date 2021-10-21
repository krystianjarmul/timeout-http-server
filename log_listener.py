import logging

import redis

from src.config import get_redis_host_and_port
from src.domain.handlers import handle_events

logger = logging.getLogger(__name__)

r = redis.Redis(**get_redis_host_and_port())


def main():
    logger.info("Redis pubsub starting")
    pubsub = r.pubsub(ignore_subscribe_messages=True)
    pubsub.subscribe("timeout")
    for msg in pubsub.listen():
        handle_events(msg)


if __name__ == '__main__':
    main()
