# Fireplace
[![Docker Repository on Quay](https://quay.io/repository/xvzf/fireplace/status "Docker Repository on Quay")](https://quay.io/repository/xvzf/fireplace)

> Start server with `python -m fireplace server`, dummy client with `python -m fireplace client`

For startup options, use the `--help` tag.


# Configuration
> A sample configuration file is located in the root folder called `test.yaml`. You can configure the application via command line options.

```
[lola ~] sudo podman run quay.io/xvzf/fireplace server --help
Usage: entrypoint.py server [OPTIONS]

  Starts server

Options:
  --config TEXT   Fireplace configuration file
  --host TEXT     Host fireplace is listening on for queries/discovery
  --port INTEGER  Port to listen on
  --help          Show this message and exit.


[lola ~] sudo podman run quay.io/xvzf/fireplace client --help
Usage: entrypoint.py client [OPTIONS]

  Starts client

Options:
  --host TEXT     Host fireplace client is listening on for queries
  --port INTEGER  Port to listen on
  --name TEXT     Name the client is using for discovery
  --server TEXT   Server address for sending discovery requests
  --help          Show this message and exit.
```

# Alerts triggered by the central (archive) server
There are two types of alerts. Each alert triggers a `POST` request to a given URL endpoint. This enables easy integration for different messaging endpoints (e.g. one processor for E-Mail, one for Telegram, ...)

Example configuration for alert targets:
```yaml
---
targets:
  - ...
    alert_targets:
      - "http://localhost:9111/postalerthere1"
      - "http://localhost:9111/postalerthere2"
```

## Unreachable Alert
This alert is triggered when the sensor is not reachable.
The `POST` data is in JSON format and has the following schema:
```json
{
  "sensor": "Sensor name",
  "event": "unreachable",
  "timestamp": "current time"
}
```

## Temperature Alert
This alert is triggered when the sensor is not reachable.
The `POST` data is in JSON format and has the following schema:
```json
{
  "sensor": "Sensor name",
  "event": "max_temp_exceeded",
  "threshold": "temperature threashold (float)",
  "measured_temp": "measured temperature which exceeded the threashold",
  "timestamp": "current time"
}
```

### Example of an incoming alert
> nc is **NOT** a valid option for receiving alerts, just for testing!
This is an alert resulting from the example configuration located at `assets/test.yaml`:
```
[lola ~] nc -l 9111
POST /email HTTP/1.1
host: localhost:9111
user-agent: python-http3/0.6.7
accept: */*
content-length: 94
accept-encoding: gzip, deflate
connection: keep-alive
content-type: application/json

{"sensor": "server1", "event": "unreachable", "timestamp": "2019-08-17T14:57:53.033172+00:00"}
```


# Getting a dev environment up and running
## Python setup
> **ATTENTION** You need at least Python 3.7 for running the server

You can use a python virtualenv for installing all dependencies:

```
# This has to be executed once
$ python -m venv --system-site-packages venv

# Active the venv
$ . ./venv/bin/activate

# Install requirements (also has to be executed once)
pip install -r requirements.txt
```

## Getting a timescaledb up and running for testing
> You can spin up a database instance using docker with ease. Please install [Docker](https://docs.docker.com/install/).
After setting up docker is done, you can spin up an instance by executing:
```
docker run -d --name timescaledb -p 127.0.0.1:5432:5432 -e POSTGRES_PASSWORD=password timescale/timescaledb:latest-pg11
```
The database has to be initialized. This can be done by this command:
```
cd assets && make
```
> Quick note: if you are running Fedora, you can swap `docker` by `sudo podman` and are good to go :-)


## Running the application inside Docker/Kubernetes
Fireplace is packed into a linux container and supposed to run as one. The image is hosted on [quay.io](https://quay.io/xvzf/fireplace)