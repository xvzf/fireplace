# fireplace.client package

## Subpackages

* fireplace.client.api package

  * Submodules

  * fireplace.client.api.configuration module

  * fireplace.client.api.containers module

  * fireplace.client.api.measurements module

  * Module contents

* fireplace.client.datastore package

  * Submodules

  * fireplace.client.datastore.buffer module

  * fireplace.client.datastore.container module

  * Module contents


## Submodules

## fireplace.client.discover module


#### fireplace.client.discover.get_config(url: str)
Retrieves the configuration from a remote server

## fireplace.client.sensor module


#### class fireplace.client.sensor.Sensor()
Bases: `object`

Interfaces the temperature sensor, dummy implementation for now


#### static read()
## Module contents


#### fireplace.client.create_client(name: str, server: str)
Dummy server for now


#### fireplace.client.setup_client(app: sanic.app.Sanic, loop: asyncio.events.AbstractEventLoop)
