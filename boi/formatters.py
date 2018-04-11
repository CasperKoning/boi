import pydoc
import json as json_lib
from pkg_resources import resource_string
from .graphics.cell_buffer import Buffer
from .item_selector import select_item
import os
import textwrap

from PIL import Image

formatter_names = ["json", "simple", "page"]

def json(items):
    print(json_lib.dumps(items, indent=2))

def simple(items):
    header = u"%3s\u2503%s\u2503%s" % ("id", "Name".center(25), "Subtitle".center(40))
    separator = (u"\u2501" * 3) + u"\u254B" + (u"\u2501" * 25) + u"\u254B" + (u"\u2501" * 40)
    def assimple(item):
        return u"%3s\u2503%s\u2503%s" %(
            item["item_id"],
            item["title"].center(25),
            item["subtitle"].center(40)
        )
    output_lines = [header, separator] + [assimple(item) for item in items]
    output = "\n".join(output_lines)
    pydoc.pager(output)


def page(items):
    def show_page(item):
        width = 100
        description_width = 55

        title = item["title"]
        subtitle = '"{}"'.format(item["subtitle"])
        types = "Type: {}".format(", ".join(item["item_types"]))
        item_pools = "Pools: {}".format(", ".join(item["item_pools"]))

        description_lines = []
        for description_part in item["description_parts"]:
            description_lines = description_lines + textwrap.fill(description_part, description_width).split("\n")

        image_path = os.path.join(os.path.split(__file__)[0], 'data/images/{}'.format(item['image_path']))
        image_height = (Image.open(image_path).size[1] // 2 + 2)

        horizontal_line = u"\u2501" * width

        header_height = sum([
            2, # top line
            2, # title
            2, # subtile
            2, # bottom line
        ])

        description_height = len(description_lines) * 2

        height = header_height + max(description_height, image_height)
    
        buffer = Buffer(width, height)
        buffer.put_line((0,0), horizontal_line)
        buffer.put_line((2,2), title)    # TODO make title more prominent
        buffer.put_line((2,4), subtitle) # TODO make title more prominent
        buffer.put_line((0,6), horizontal_line)
        buffer.put_line((30, 2), types)
        buffer.put_line((30, 4), item_pools)
        for index, line in enumerate(description_lines):
            buffer.put_line((2,7 + (2*index)), line)

        buffer.put_image(image_path, description_width + 10, header_height + 10, (255, 255, 255))

        buffer.display()
    
    if len(items) > 1:
        item = select_item(items)
        show_page(item)
    else:
        show_page(items[0])
    
formatters = {
    "json": json,
    "simple": simple,
    "page": page
}
