import asyncio
from time import sleep
import fireplace

async def main():
    sensor = fireplace.client.sensor.Sensor()
    fireplace.logger.info(f"Temperature: {await sensor.get_temperature()}")

if __name__ == "__main__":
    asyncio.get_event_loop().run_until_complete(main())