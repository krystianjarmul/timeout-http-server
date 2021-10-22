import logging
import os

logging.basicConfig(
    level=logging.INFO, format=f"%(levelname)s:     %(message)s"
)
uvicorn_logger = logging.getLogger('uvicorn.error')
uvicorn_logger.propagate = False


def get_redis_host_and_port():
    host = os.environ.get("REDIS_HOST", "localhost")
    port = 63791 if host == "localhost" else 6379
    return dict(host=host, port=port)
