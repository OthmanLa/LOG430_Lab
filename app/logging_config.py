import logging
from pythonjsonlogger import jsonlogger

def setup_logging():
    # Handler sur stdout
    handler = logging.StreamHandler()
    fmt = jsonlogger.JsonFormatter(
        '%(asctime)s %(levelname)s %(name)s %(message_id)s %(message)s'
    )
    handler.setFormatter(fmt)
    root = logging.getLogger()
    root.setLevel(logging.INFO)
    root.handlers = [handler]
