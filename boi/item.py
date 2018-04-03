import click
import json
from pkg_resources import resource_string
from .formatters import formatter_names
from .formatters import formatters

@click.group()
def item():
    """
    Get details regarding items
    """
    pass

@item.command()
@click.option("-f", "--format", metavar="FORMAT", default="simple", type=click.Choice(formatter_names), help="Output format (can be %s)." % ", ".join(formatter_names))
def all(format):
    """
    Lists all items
    """
    items = json.loads(resource_string(__name__, 'data/items.json'))
    formatters[format](items)

@item.command()
@click.argument("id")
@click.option("-f", "--format", metavar="FORMAT", default="simple", type=click.Choice(formatter_names), help="Output format (can be %s)." % ", ".join(formatter_names))
def id(id, format):
    """
    Find an item by its ID and display its information
    """
    items = json.loads(resource_string(__name__, 'data/items.json'))
    results = []
    for item in items:
        if item['item_id'] == id:
            results.append(item)
            break
    else:
        print("Could not find an item with id {}".format(id))
    formatters[format](results)

@item.command()
@click.argument("search_term")
@click.option("-f", "--format", metavar="FORMAT", default="simple", type=click.Choice(formatter_names), help="Output format (can be %s)." % ", ".join(formatter_names))
def search(search_term, format):
    """
    Find an item via a search term (name, subtitle, some property)
    """
    items = json.loads(resource_string(__name__, 'data/items.json'))
    results = []
    st = search_term.lower()
    def has_search_term(item, search_term):
        if search_term in item["title"].lower() or search_term in item["subtitle"].lower():
            return True
        search_tags = item["search_tags"]
        for tag in search_tags:
            if search_term in tag:
                return True
        else:
            return False

    for item in items:
        if has_search_term(item, st):
            results.append(item)
    if results:
        formatters[format](results)
    else:
        print("Could not find an item for the search term {}".format(search_term))
