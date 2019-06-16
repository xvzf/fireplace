import logging
from dataclasses import dataclass
from typing import List
from yaml import load
from pprint import pprint
try:
    from yaml import CLoader as Loader, CDumper as Dumper
except ImportError:
    from yaml import Loader, Dumper

# Set debug level for now
logging.basicConfig(
    format="%(asctime)s [%(levelname)s] %(message)s", level=logging.DEBUG)
logger = logging.getLogger(__name__)


@dataclass
class Config:
    """ Config store """
    # List of all targets
    targets: List[str]
    # Scrape interval
    scrape_interval: float = 10.0


def load_config(path: str) -> Config:
    """ Load configuration

    @param path: Path of the configuration file
    @returns: Config object
    """
    with open(path, "r") as cfg:
        l = load(cfg, Loader=Loader)
        config = Config(**l)
        logger.info(f"Loaded config {path}")
        return config