from datetime import datetime


class Metric:
    """ Metric data structure for API doc """
    time = datetime
    name = str
    temperature = float


class Statistics:
    """ Statistics data structure for API doc """
    time = int
    min_temperature = float
    max_temperature = float
    avg_temperature = float