import struct
import random
from . import AbstractSensor
from . import Countermeasure
from .. import logger
try:
    import smbus

    class Sensor(AbstractSensor):
        """ Reads the temperature sensor """

        reg_temp = 0xaa
        reg_config = 0x01

        def __init__(self, channel=1, sensor_addr=0x48):
            """ Initializes the sensor

            :param channel: I2C Bus Channel
            :param sensor_addr: Sensor address
            """
            self.bus = smbus.SMBus(channel)
            self.sensor_addr = 0x48


        async def get_temperature(self):
            """ Reads the temperature sensor """
            # Read the register containing the temperature (2 bytes)
            recv_buf = self.bus.read_i2c_block_data(
                self.sensor_addr, self.reg_temp, 2)

            # Little endian short, see https://docs.python.org/3/library/struct.html#format-characters
            return struct.unpack("<h", bytes(recv_buf))[0]
            
            # Hier die Gegenmassnahme starten falls Temperatur zu hoch? Wie komme ich an die Maximaltemperatur?

            # Hier die Gegenmassnahme stoppen falls die Temperatur wieder unter der Maximaltemperatur liegt
except:
    logger.warn("smbus library is not available/installed, fallback to dummy sensor")

    class Sensor(AbstractSensor):

        async def get_temperature(self):
            return random.randint(2000, 4000) / 100.0
