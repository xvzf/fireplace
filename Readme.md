# Fireplace
> Start server with `python -m fireplace server`, dummy client with `python -m fireplace client`

For startup options, use the `--help` tag.


# Configuration
> A sample configuration file is located in the root folder called `test.yaml` - setting its path via environment variables is on the TODO list


# Getting a dev environment up and running
## Python setup
> **ATTENTION** You need at least Python 3.5 for running the server

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
