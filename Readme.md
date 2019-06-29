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
> Quick note: if you are running Fedora, you can swap `docker` by `sudo podman` and are good to go :-)


## Running the application inside Docker/Kubernetes
Fireplace is packed into a linux container and supposed to run as one. The image is hosted on [quay.io](https://quay.io/xvzf/fireplace)