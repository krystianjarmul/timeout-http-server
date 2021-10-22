import redis

from timeout.config import get_redis_host_and_port
from timeout.domain.handlers import handle_events, logger


r = redis.Redis(**get_redis_host_and_port())


def listen():
    logger.info("Redis pubsub starting")
    pubsub = r.pubsub(ignore_subscribe_messages=True)
    pubsub.subscribe("timeout")
    for msg in pubsub.listen():
        handle_events(msg)


if __name__ == '__main__':
    listen()
