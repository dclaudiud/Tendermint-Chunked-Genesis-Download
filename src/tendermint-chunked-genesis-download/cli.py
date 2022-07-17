import click
from download_genesis import *


# printing the errors with red
def __print_err__(text):
    print('\033[38;2;{};{};{}m{} \033[38;2;255;255;255m'.format(255, 0, 0, text))
    exit(1)


@click.command()
@click.argument('url', default=None, help="Tendermint RPC url")
def main(url):
    try:
        download_genesis(url)
    except (InvalidRPC, NodeNotSynchronized, UnsuccessfulHttpRequest) as e:
        __print_err__(e.message)
    except Exception as e:
        __print_err__(getattr(e, 'message', str(e)))

    exit(0)
