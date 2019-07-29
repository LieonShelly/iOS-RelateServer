import logging
import logging.handlers
from flask import Blueprint

log_api = Blueprint('log_api', __name__)

from . import Route

logger = logging.getLogger(__name__)
logger.setLevel(level=logging.DEBUG)
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
stream_handler = logging.StreamHandler()
stream_handler.setFormatter(formatter)
logger.addHandler(stream_handler)
rt_file_handler = logging.handlers.RotatingFileHandler(filename='output.log', maxBytes=10 * 1024 * 1024, backupCount=1)
rt_file_handler.setFormatter(formatter)
logger.addHandler(rt_file_handler)