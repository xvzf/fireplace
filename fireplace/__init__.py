import logging

# Set debug level for now
logging.basicConfig(
    format="%(asctime)s [%(levelname)s] %(message)s", level=logging.DEBUG)
logger = logging.getLogger(__name__)

from . import server
from . import client
from . import scheduler
from . import helper
from . import config