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
class Database:
    """ Database config store """
    host: str
    user: str
    password: str
    database: str


@dataclass
class Target:
    """ target config store """
    url: str
    threshold: float
    name: str
    every: float


class Config:
    """ Config store """

    # List of all targets
    targets: List[Target]
    # Database connection settings
    database: Database
    # Scrape interval
    scrape_interval: float

    def __init__(self, targets: List[dict], database: dict, scrape_interval: float = 10):
        """ Initialize config """
        self.scrape_interval = scrape_interval
        self.database = database
        self.targets = []
        # Workaround until nested dataclasses are working :)
        for target in targets:
            self.targets.append(Target(**target))


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


config = Config(targets=[], database={
    "user": "none",
    "password": "none",
    "database": "none"
})
