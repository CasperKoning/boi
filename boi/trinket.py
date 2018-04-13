import click
import json
from pkg_resources import resource_string
from .formatters import formatter_names
from .formatters import formatters
from .item_selector import select_item

@click.group()
def trinket():
    """
    Get details regarding trinkets
    """
    pass

@trinket.command()
@click.option("-f", "--format", metavar="FORMAT", default="simple", type=click.Choice(formatter_names), help="Output format (can be %s)." % ", ".join(formatter_names))
def all(format):
    """
    Lists all trinkets
    """
    trinkets = json.loads(resource_string(__name__, 'data/trinkets.json')).values()
    formatters[format](trinkets)

@trinket.command()
@click.argument("id")
@click.option("-f", "--format", metavar="FORMAT", default="page", type=click.Choice(formatter_names), help="Output format (can be %s)." % ", ".join(formatter_names))
def id(id, format):
    """
    Find a trinket by its ID and display its information
    """
    trinkets = json.loads(resource_string(__name__, 'data/trinkets.json')).values()
    results = []
    for trinket in trinkets:
        if trinket['item_id'] == id:
            results.append(trinket)
            break
    else:
        print("Could not find an item with id {}".format(id))
    formatters[format](results)

@trinket.command()
@click.argument("search_term")
@click.option("-f", "--format", metavar="FORMAT", default="page", type=click.Choice(formatter_names), help="Output format (can be %s)." % ", ".join(formatter_names))
def search(search_term, format):
    """
    Find a trinket via a search term (name, subtitle, some property)
    """
    trinkets = json.loads(resource_string(__name__, 'data/trinkets.json')).values()
    results = []
    st = search_term.lower()
    def has_search_term(trinket, search_term):
        if search_term in trinket["title"].lower() or search_term in trinket["subtitle"].lower():
            return True
        search_tags = trinket["search_tags"]
        for tag in search_tags:
            if search_term in tag:
                return True
        else:
            return False

    for trinket in trinkets:
        if has_search_term(trinket, st):
            results.append(trinket)
    if results:
        formatters[format](results)
    else:
        print("Could not find a trinket for the search term {}".format(search_term))
