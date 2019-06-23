# fireplace.server.api package

## Submodules

## fireplace.server.api.containers module


#### class fireplace.server.api.containers.Metric()
Bases: `object`

Metric data structure for API doc


#### name()
alias of `builtins.str`


#### temperature()
alias of `builtins.float`


#### time()
alias of `datetime.datetime`


#### class fireplace.server.api.containers.Statistics()
Bases: `object`

Statistics data structure for API doc


#### avg_temperature()
alias of `builtins.float`


#### max_temperature()
alias of `builtins.float`


#### min_temperature()
alias of `builtins.float`


#### time()
alias of `builtins.int`

## fireplace.server.api.query module


#### fireplace.server.api.query.get_current_temp(request, target)

#### fireplace.server.api.query.get_stats(request, target: str, interval: int, offset: int, latest: int)
## Module contents
