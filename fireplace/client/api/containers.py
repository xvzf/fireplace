from datetime import datetime


class Target:
    url = str
    threshold = float
    name = str
    every = float


class Measurement:
    time = datetime
    temperature = float
