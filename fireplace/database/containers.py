from dataclasses import dataclass
from datetime import datetime

@dataclass
class Metric:
    """ Metric timepoint
    
    !!! if you change the datatypes of this class, adapt MetricMeta !!!
    """
    time: datetime
    name: str
    temperature: float


@dataclass
class Statistics:
    """ Target statistics """
    time: datetime
    min_temperature: float
    max_temperature: float
    avg_temperature: float
