# -*- coding: utf-8 -*-

# Adapted from github.com/Tenchi2xh/pokedex-cli/blob/b71a205/pokedex/graphics/cell_buffer.py

from __future__ import print_function

from .colors import *

import collections

from PIL import Image

from math import ceil

Cell = collections.namedtuple("Cell", "character fg bg")

block_top = "▀"

class Buffer(object):
    def __init__(self, width=80, height=16):
        self.width = width
        self.height = height
        self.buffer = [[Cell(" ", 15, -1) for x in range(width)] for y in range(height)]

    def put_cell(self, position, character, fg=15, bg=-1):
        x, y = position
        assert x >= 0
        assert y >= 0
        assert x < self.width
        assert y < self.height
        assert len(character) > 0
        self.buffer[y][x] = Cell(character, fg, bg)

    def put_line(self, position, line, fg=15, bg=-1):
        x, y = position
        for i, char in enumerate(line):
            self.put_cell((x+i, y), char, fg, bg)

    def put_image(self, path, image_dimensions, offset = (0,0), transparent_replacement=(255, 255, 255)):
        def get_pixels(path, image_dimensions, transparent_replacement):
            image = Image.open(path)
            image.thumbnail(image_dimensions)
            image = image.convert("RGBA")
            background = Image.new("RGBA", image_dimensions, transparent_replacement)
            centering_x_offset = max(0, (image_dimensions[0] - image.size[0]) // 2)
            centering_y_offset = max(0, (image_dimensions[1] - image.size[1]) // 2)
            background.paste(image, (centering_x_offset, centering_y_offset), image)
            return background.convert("RGB").load()

        x0, y0 = offset[0], offset[1]
        width, height = image_dimensions[0], image_dimensions[1]
        
        pixels = get_pixels(path, image_dimensions, transparent_replacement)

        for y in range(0, height, 2):
            for x in range(width):
                color_top = rgb_to_xterm(pixels[x, y])
                color_bottom = rgb_to_xterm(pixels[x, y + 1])
                self.put_cell((x0 + x, y0 + y // 2), block_top, color_top, color_bottom)

    def render(self):
        output = []
        for line in self.buffer:
            result = ""
            last_fg, last_bg = -1, -1

            for cell in line:
                if cell.fg != last_fg:
                    result += format_fg(cell.fg)
                    last_fg = cell.fg
                if cell.bg != last_bg:
                    result += format_bg(cell.bg)
                    last_bg = cell.bg
                result += cell.character
            result += reset_code
            output.append(result)

        return output

    def display(self):
        print()
        for line in self.render():
            print(line)
