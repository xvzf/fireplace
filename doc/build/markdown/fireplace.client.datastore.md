# fireplace.client.datastore package

## Submodules

## fireplace.client.datastore.buffer module


#### class fireplace.client.datastore.buffer.MeasurementBuffer(max_buf_size=3600)
Bases: `object`

Ring buffer for storing measurements


#### add(datapoint: fireplace.client.datastore.container.Measurement)
Adds an element to the ring buffer

@param datapoint: Measurement to store


#### get_from(from_time: datetime.datetime)
Retrieves data from a giving timestamp

@param from_time: Return all measurements later than from_time

## fireplace.client.datastore.container module


#### class fireplace.client.datastore.container.Measurement(time: datetime.datetime, temperature: float)
Bases: `object`

## Module contents
