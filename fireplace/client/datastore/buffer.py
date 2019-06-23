import collections
import pytz
from datetime import datetime
from typing import List
from . import container


class MeasurementBuffer:
    """ Ring buffer for storing measurements """

    def __init__(self, max_buf_size=3600):
        """ Initialize ring buffer

        :param max_buf_size: Max buffer size before elements get dropped
        """
        self.ring = collections.deque(maxlen=max_buf_size)

    def add(self, datapoint: container.Measurement):
        """ Adds an element to the ring buffer
        
        :param datapoint: Measurement to store
        """
        self.ring.append(datapoint)

    def get_from(self, from_time: datetime) -> List[container.Measurement]:
        """ Retrieves data from a giving timestamp

        :param from_time: Return all measurements later than from_time
        """
        self.ring.reverse()  # In place, relevant values are found first

        tmp = collections.deque()

        for m in self.ring:
            timediff = m.time.replace(tzinfo=pytz.utc) - from_time.replace(tzinfo=pytz.utc)
            if timediff.total_seconds() < 0:
                # Measurement is older than start time and not requested
                break
            tmp.appendleft(m)

        self.ring.reverse()  # undo the previous reverse
        return tmp
