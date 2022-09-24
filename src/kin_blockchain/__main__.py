import os

import click
import uvicorn


@click.group()
def cli():
    pass


@cli.command()
def run_server():
    options = {
        "host": os.environ.get("GUNICORN_HOST", "0.0.0.0"),
        "port": os.environ.get("GUNICORN_PORT", 8000),
        "log_level": "debug",
        "workers": 1,
        "reload": True,
    }

    uvicorn.run("kin_blockchain.app:create_app", **options)


if __name__ == '__main__':
    cli()
