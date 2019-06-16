# fireplace package

## Subpackages

* fireplace.client package

  * Subpackages

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

  * Submodules

  * fireplace.client.discover module

  * fireplace.client.sensor module

  * Module contents

* fireplace.helper package

  * Submodules

  * fireplace.helper.api module

  * fireplace.helper.json module

  * Module contents

* fireplace.scheduler package

  * Submodules

  * fireplace.scheduler.async_scheduler module

  * Module contents

* fireplace.server package

  * Subpackages

    * fireplace.server.api package

      * Submodules

      * fireplace.server.api.containers module

      * fireplace.server.api.query module

      * Module contents

    * fireplace.server.database package

      * Submodules

      * fireplace.server.database.containers module

      * fireplace.server.database.dao module

      * fireplace.server.database.mapper module

      * Module contents

    * fireplace.server.discovery package

      * Submodules

      * fireplace.server.discovery.containers module

      * fireplace.server.discovery.endpoint module

      * Module contents

  * Submodules

  * fireplace.server.scraper module

  * Module contents


## Submodules

## fireplace.config module


#### class fireplace.config.Config(targets: List[dict], database: dict, scrape_interval: float = 10)
Bases: `object`

Config store


#### class fireplace.config.Database(host: str, user: str, password: str, database: str)
Bases: `object`

Database config store


#### class fireplace.config.Target(url: str, threshold: float, name: str, every: float)
Bases: `object`

target config store


#### fireplace.config.load_config(app: sanic.app.Sanic, path: str)
Load configuration

@param path: Path of the configuration file
@returns: Config object

## Module contents
