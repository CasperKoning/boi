import click
import json
from pkg_resources import resource_string
import pydoc


@click.group()
def item():
    """
    Get details regarding items
    """
    pass

@item.command()
def all():
    """
    Lists all items
    """
    items = json.loads(resource_string(__name__, 'data/items.json'))
    pydoc.pager(json.dumps(items, indent=2))

@item.command()
@click.argument("id")
def id(id):
    """
    Find an item by its ID and display its information
    """
    items = json.loads(resource_string(__name__, 'data/items.json'))
    for item in items:
        if item['item_id'] == id:
            pydoc.pager(json.dumps(item, indent=2))
            break
    else:
        print("Could not find an item with id {}".format(id))

@item.command()
@click.argument("search_term")
def search(search_term):
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
        pydoc.pager(json.dumps(results, indent=2))
    else:
        print("Could not find an item for the search term {}".format(search_term))
