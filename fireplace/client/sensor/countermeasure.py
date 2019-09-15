import struct
import random
from .. import logger
try:
    import smbus

    class Countermeasure():
        """ Starts and stops the connected fan """

        reg_config_fanLedOn = 0x09
        reg_config_fanOn = 0x08
        reg_config_fanOff = 0x00

        def __init__(self, channel=1, fan_addr=0x20):
            """ Initializes the sensor

            :param channel: I2C Bus Channel
            :param sensor_addr: Sensor address
            """
            self.bus = smbus.SMBus(channel)
            self.fan_addr = 0x20

        async def start_fan(self):
            self.bus.write_byte(self.fan_addr, self.reg_config_fanLedOn)

        async def stop_fan(self):
            self.bus.write_byte(self.fan_addr, self.reg_config_fanOff)

except:
    logger.warn("smbus library is not available/installed")

