#!/usr/bin/python

from urllib2 import urlopen
from lxml import html
import requests
import shutil
import json
import progressbar


def extract_item_info(item, item_types=[]):
    item_id = (item.xpath('./@data-sid'))[0]

    title = (item.xpath('.//p[@class="item-title"]/text()') or [""])[0]

    subtitle = (item.xpath('.//p[@class="pickup"]/text()') or [""])[0].replace("\"", "")

    description_parts = []
    description_lines = item.xpath(u'.//p[starts-with(text(), "\u2022")]/text()')
    for line in description_lines:
        splits = line.split("\n")
        rejoined = " ".join([split.replace(u"\u2022", "").strip() for split in splits])
        description_parts.append(rejoined)
    description_parts = [part.strip() for part in description_parts if part.strip()]

    item_pools = (item.xpath('.//p[starts-with(text(), "Item Pool")]/text()') or [""])[0].replace("Item Pool:", "")
    item_pools = [item_pool.strip() for item_pool in item_pools.split(",")]
    item_pools = filter(lambda item_pool: not (item_pool == ""), item_pools)

    item_types = (item_types or item.xpath('.//p[starts-with(text(), "Type")]/text()') or [""])[0].replace("Type:", "")
    item_types = [item_type.strip() for item_type in item_types.split(",")]
    item_types = filter(lambda item_type: not (item_type == ""), item_types)

    search_tags = (item.xpath('.//p[@class="tags"]/text()') or [""])[0]
    search_tags = [tag.strip() for tag in search_tags.split(",")]
    search_tags = filter(lambda tag: not (tag == "" or "*" in tag), search_tags)

    info = {
        "item_id": item_id,
        "title": title,
        "subtitle": subtitle,
        "description_parts": description_parts,
        "item_pools": item_pools,
        "item_types": item_types,
        "search_tags": search_tags
    }
    return info

platinumgod_content = html.parse('http://platinumgod.co.uk')

print("Extracting image information")
item_containers = platinumgod_content.xpath('//div[contains(@class, "items-container")]')
item_infos = []
for item_container in item_containers:
    items = item_container.xpath('.//li[contains(@class, "textbox")]')
    bar = progressbar.ProgressBar()
    for item in bar(items):
        item_info = extract_item_info(item)
        item_infos.append(item_info)

with open("../data/items.json", "w") as f:
    json.dump(item_infos, f)

print("Extracting trinket information")
trinket_containers = platinumgod_content.xpath('//div[contains(@class, "trinkets-container")]')
trinket_infos = []
for trinket_container in trinket_containers:
    trinkets = trinket_container.xpath('.//li[contains(@class, "textbox")]')
    bar = progressbar.ProgressBar()
    for trinket in bar(trinkets):
        trinket_info = extract_item_info(trinket, item_types=["Trinket"])
        trinket_infos.append(trinket_info)

with open("../data/trinkets.json", "w") as f:
    json.dump(trinket_infos, f)

print("Extracting images for items")
boi_wiki_items_content = html.parse(urlopen('https://bindingofisaacrebirth.gamepedia.com/Item'))  # urlopen needed because op https...
item_categories = boi_wiki_items_content.xpath('//table[contains(@class, "table-item")]')
for item_category in item_categories:
    items = item_category.xpath('./tr[position()>1]')
    bar = progressbar.ProgressBar()
    for item in bar(items):
        item_id = (item.xpath('./td[2]/text()') or [""])[0].strip()
        image_url = (item.xpath('./td[3]')[0].xpath('./a/img/@src') or item.xpath('./td[3]')[0].xpath('./div/a/img/@src') or [""])[0].strip()
        response = requests.get(image_url, stream=True)
        with open('../data/images/items/{}.png'.format(item_id), 'wb') as out_file:
            shutil.copyfileobj(response.raw, out_file)
        del response

print("Extracting images for trinkets")
boi_wiki_trinkets_content = html.parse(urlopen('https://bindingofisaacrebirth.gamepedia.com/Trinkets'))  # urlopen needed because op https...
trinket_categories = boi_wiki_trinkets_content.xpath('//table[contains(@class, "trinkets")]')
for trinket_category in trinket_categories:
    trinkets = trinket_category.xpath('./tr[position()>1]')
    bar = progressbar.ProgressBar()
    for trinket in bar(trinkets):
        trinket_id = (trinket.xpath('./td[2]/text()') or [""])[0].strip()
        image_url = (trinket.xpath('./td[3]')[0].xpath('./a/img/@src') or trinket.xpath('./td[3]')[0].xpath('./div/a/img/@src') or [""])[0].strip()
        response = requests.get(image_url, stream=True)
        with open('../data/images/trinkets/{}.png'.format(trinket_id), 'wb') as out_file:
            shutil.copyfileobj(response.raw, out_file)
        del response
