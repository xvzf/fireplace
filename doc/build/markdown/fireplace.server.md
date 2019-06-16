# fireplace.server package

## Subpackages

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


## Submodules

## fireplace.server.scraper module


#### exception fireplace.server.scraper.ScrapeException()
Bases: `Exception`


#### class fireplace.server.scraper.Scraper()
Bases: `object`


#### static get_handler(app: sanic.app.Sanic, target: fireplace.config.Target)
Generats the async scrape function which handles *EVERYTHING*


#### static read_sensor(target: fireplace.config.Target, last_scraped: datetime.datetime)
Retrieve sensor data from a target (IPv4, IPv6 or DNS)

@param target: Target address
@returns: {temperature: …}

## Module contents


#### fireplace.server.create_server(config_path: str)
