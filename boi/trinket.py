import click
import json
from pkg_resources import resource_string


@click.group()
def trinket():
    """
    Get details regarding trinkets
    """
    pass

@trinket.command()
def all():
    """
    Lists all trinkets
    """
    trinkets = json.loads(resource_string(__name__, 'data/trinkets.json'))
    print(json.dumps(trinkets, indent=2))

@trinket.command()
@click.argument("id")
def id(id):
    """
    Find a trinket by its ID and display its information
    """
    trinkets = json.loads(resource_string(__name__, 'data/trinkets.json'))
    for trinket in trinkets:
        if trinket['item_id'] == id:
            print(json.dumps(trinket, indent=2))
            break
    else:
        print("Could not find an item with id {}".format(id))

@trinket.command()
@click.argument("search_term")
def search(search_term):
    """
    Find a trinket via a search term (name, subtitle, some property)
    """
    trinkets = json.loads(resource_string(__name__, 'data/trinkets.json'))
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
        print(json.dumps(results, indent=2))
    else:
        print("Could not find an item for the search term {}".format(search_term))
