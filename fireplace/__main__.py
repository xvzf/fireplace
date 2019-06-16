import click
from .server import create_server
from .client import create_client


@click.group()
def cli():
    pass


@cli.command()
@click.option("--config", default="assets/test.yaml", help="Fireplace configuration file")
@click.option("--host", default="::", help="Host fireplace is listening on for queries/discovery")
@click.option("--port", default=8080, help="Port to listen on")
def server(config: str, host: str, port: int):
    """ Starts server """
    app = create_server(config)
    app.run(host=host, port=port)


@cli.command()
@click.option("--host", default="::", help="Host fireplace client is listening on for queries")
@click.option("--port", default=9000, help="Port to listen on")
@click.option("--name", default="dont_use_this_name", help="Name the client is using for discovery")
@click.option("--server", default="http://localhost:8080/discovery/", help="Server address for sending discovery requests")
def client(host: str, port: int, name: str, server: str):
    """ Starts client """
    app = create_client(name, server + name)
    app.run(host=host, port=port)


if __name__ == "__main__":
    cli()
