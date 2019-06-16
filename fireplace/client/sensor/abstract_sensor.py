from datetime import datetime
from abc import ABC, abstractclassmethod

class AbstractSensor(ABC):
    """ Basic interface """

    @abstractclassmethod
    async def get_temperature(self):
        """ Retrieve the current temperature from the sensor """
        raise NotImplementedError