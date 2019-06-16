from datetime import datetime
from dataclasses import dataclass


@dataclass
class Measurement:
    time: datetime
    temperature: float
