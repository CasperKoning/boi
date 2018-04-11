# -*- coding: utf-8 -*-

# Adapted from https://github.com/Tenchi2xh/pokedex-cli/blob/b71a205/pokedex/graphics/colors.py

from .conversion import rgb2short

def rgb_to_xterm(color):
    hex_color = "%02x%02x%02x" % color
    return int(rgb2short(hex_color)[0])

reset_code = "\033[0m"

def format_fg(fg):
    return "\033[38;5;%dm" % fg

def format_bg(bg):
    if bg == -1:
        return "\033[49m"
    return "\033[48;5;%dm" % bg
