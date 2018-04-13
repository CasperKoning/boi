import pydoc
import json as json_lib
from pkg_resources import resource_string
from .graphics.cell_buffer import Buffer
from .item_selector import select_item
import os
import textwrap
from math import ceil

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
        description_width = 52
        image_height = 26
        image_width = 26
        horizontal_component_dist = 2
        horizontal_outline_dist = 2
        vertical_outline_dist = 1
        width = 1 + horizontal_outline_dist + description_width + horizontal_component_dist + image_width + horizontal_outline_dist + 1

        title = item["title"]
        subtitle = '"{}"'.format(item["subtitle"])
        item_types = "Type: {}".format(", ".join(item["item_types"]))
        item_pools = "Pools: {}".format(", ".join(item["item_pools"]))

        description_parts = item["description_parts"]
        description_parts = [val for pair in zip(description_parts, ["\n"] * len(description_parts)) for val in pair] # interleave lines with newlines
        description_parts = description_parts[:-1] # drop last newline

        description_lines = []
        for description_part in description_parts:
            description_lines = description_lines + textwrap.fill(description_part, description_width).split("\n")

        image_path = os.path.join(os.path.split(__file__)[0], 'data/images/{}'.format(item['image_path']))

        header_height = sum([
            1, # top line
            vertical_outline_dist,
            1, # title
            1, # empty line
            1, # subtitle
            vertical_outline_dist,
            1, # bottom line
        ])

        description_height = len(description_lines)
        
        height = header_height + vertical_outline_dist + max(description_height, ceil(image_height // 2)) + vertical_outline_dist + 1 # height // 2 because we draw two pixels in the vertical direction with one box character
    
        def put_outline(buffer):
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
            buffer.put_line((1 + horizontal_outline_dist, 1 + vertical_outline_dist), title)
            buffer.put_line((1 + horizontal_outline_dist, 1 + 2 + vertical_outline_dist), subtitle)
            buffer.put_line((30, 1 + vertical_outline_dist), item_types)
            buffer.put_line((30, 1 + 2 + vertical_outline_dist), item_pools)

        def put_description_text(buffer, description_lines):
            for index, line in enumerate(description_lines):
                buffer.put_line((1 + horizontal_outline_dist, header_height + vertical_outline_dist + index), line)

        def put_description_image(buffer, image_path):
            buffer.put_image(image_path, (image_width, image_height), (1 + horizontal_outline_dist + description_width + horizontal_component_dist, header_height + vertical_outline_dist), (255, 255, 255))

        buffer = Buffer(width, height)

        put_outline(buffer)
        put_header_content(buffer, title, subtitle, item_types, item_pools)
        put_description_text(buffer, description_lines)
        put_description_image(buffer, image_path)

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
