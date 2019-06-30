import smbus
import struct
from . import AbstractSensor
from .. import logger


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

    def get_temperature(self):
        """ Reads the temperature sensor """
        # Read the register containing the temperature (2 bytes)
        recv_buf = self.bus.read_i2c_block_data(
            self.sensor_addr, self.reg_temp, 2)

        # Little endian short, see https://docs.python.org/3/library/struct.html#format-characters
        return struct.unpack("<h", recv_buf)[0] * 0.0625
