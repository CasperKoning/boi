import click

from .item import item
from .trinket import trinket

@click.group()
def boi():
    """
    boi - Command line interface for discovering Binding of Isaac details
    """
    pass

boi.add_command(item)
boi.add_command(trinket)


if __name__ == "__main__":
    boi()