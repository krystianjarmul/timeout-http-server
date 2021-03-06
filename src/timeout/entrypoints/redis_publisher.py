import json

import redis

from timeout.config import get_redis_host_and_port
from timeout.domain.events import Event

r = redis.Redis(**get_redis_host_and_port())


def publish(channel: str, event: Event):
    data = vars(event)
    message = json.dumps(data)
    r.publish(channel=channel, message=message)
