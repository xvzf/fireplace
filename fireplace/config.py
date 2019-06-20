from dataclasses import dataclass
from typing import List


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
