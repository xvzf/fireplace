import click
from .server import create_server


@click.group()
def cli():
    pass


@cli.command()
@click.option("--config", default="assets/test.yaml", help="Fireplace configuration file")
@click.option("--host", default="::", help="Host fireplace is listening on for queries/discovery")
@click.option("--port", default=8080, help="Port to listen on")
def server(config: str, host: str, port: int):
    """ Startup server """
    app = create_server(config)
    app.run(host=host, port=port)


if __name__ == "__main__":
    cli()
