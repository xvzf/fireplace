import logging
import asyncpg
from yaml import load
try:
    from yaml import CLoader as Loader, CDumper as Dumper
except ImportError:
    from yaml import Loader, Dumper
from .config import Config, Database, Target


# Set debug level for now
logging.basicConfig(
    format="%(asctime)s [%(levelname)s] %(message)s", level=logging.DEBUG)
logger = logging.getLogger(__name__)


# To be filled after initialization :-)
config: Config = None


def load_config(path: str) -> Config:
    """ Load configuration

    @param path: Path of the configuration file
    @returns: Config object
    """
    global config
    with open(path, "r") as cfg:
        l = load(cfg, Loader=Loader)
        config = Config(**l)
        logger.info(f"Loaded config {path}")
        return config
