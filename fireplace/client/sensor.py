import random

class Sensor:
    """ Interfaces the temperature sensor, dummy implementation for now """

    @staticmethod
    async def read() -> float:
        return random.randint(2000, 4000) / 100.0