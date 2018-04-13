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
    def put_outline(buffer, width, height, header_height):
        horizontal_line = u"\u2501" * (width - 2)

        buffer.put_cell((0, 0), u"\u250F")
        buffer.put_line((1, 0), horizontal_line)
        buffer.put_cell((width - 1, 0), u"\u2513")

        for i in range(1, header_height):
            buffer.put_cell((0, i), u"\u2503")
            buffer.put_cell((width - 1, i), u"\u2503")
        
        buffer.put_cell((0, header_height - 1), u"\u2523")
        buffer.put_cell((width - 1, header_height - 1), u"\u252B")
        buffer.put_line((1, header_height - 1), horizontal_line)

        for i in range(header_height, height - 1):
            buffer.put_cell((0, i), u"\u2503")
            buffer.put_cell((width - 1, i), u"\u2503")

        buffer.put_cell((0, height - 1), u"\u2517")
        buffer.put_cell((width - 1, height - 1), u"\u251B")
        buffer.put_line((1, height - 1), horizontal_line)

    def put_header_content(buffer, title, subtitle, item_types, item_pools):
        buffer.put_line((2, 1), title)
        buffer.put_line((2, 3), subtitle)
        buffer.put_line((30, 1), item_types)
        buffer.put_line((30, 3), item_pools)

    def put_description_text(buffer, header_height, description_width, description_lines):
        for index, line in enumerate(description_lines):
            buffer.put_line((2, header_height + (2 * index)), line)

    def put_description_image(buffer, header_height, description_width, image_width, image_height, image_path):
        buffer.put_image(image_path, (image_width, image_height), (description_width + 5, header_height + 1), (255, 255, 255))

    def show_page(item):
        width = 100
        description_width = 55
        image_height = 26
        image_width = 26

        title = item["title"]
        subtitle = '"{}"'.format(item["subtitle"])
        item_types = "Type: {}".format(", ".join(item["item_types"]))
        item_pools = "Pools: {}".format(", ".join(item["item_pools"]))

        description_lines = []
        for description_part in item["description_parts"]:
            description_lines = description_lines + textwrap.fill(description_part, description_width).split("\n")

        image_path = os.path.join(os.path.split(__file__)[0], 'data/images/{}'.format(item['image_path']))

        header_height = sum([
            1, # top line
            2, # title
            2, # subtile
            1, # bottom line
        ])

        description_height = len(description_lines) * 2

        height = header_height + max(description_height, image_height) + 2
    
        buffer = Buffer(width, height)

        put_outline(buffer, width, height, header_height)
        put_header_content(buffer, title, subtitle, item_types, item_pools)
        put_description_text(buffer, header_height, description_width, description_lines)
        put_description_image(buffer, header_height, description_width, image_height, image_width, image_path)

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
