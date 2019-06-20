# Fireplace
> Start server with `python -m fireplace`

# Configuration
> A sample configuration file is located in the root folder called `test.yaml` - setting its path via environment variables is on the TODO list

# Getting a dev environment up and running
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
