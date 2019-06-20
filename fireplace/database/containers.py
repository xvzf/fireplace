from dataclasses import dataclass
from datetime import datetime

@dataclass
class Metric:
    """ Metric timepoint """
    time: datetime
    name: str
    temperature: float