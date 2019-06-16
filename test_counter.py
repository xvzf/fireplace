import asyncio
from time import sleep
import fireplace

async def main():
    fan = fireplace.client.Countermeasure()

    await fan.start_fan()
    await asyncio.sleep(10)
    await fan.stop_fan()

if __name__ == "__main__":
    asyncio.get_event_loop().run_until_complete(main())
