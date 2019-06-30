from time import sleep
import fireplace

if __name__ == "__main__":
    sensor = fireplace.client.sensor.Sensor()
    fireplace.logger.info(f"Temperature: {sensor.get_temperature()}")