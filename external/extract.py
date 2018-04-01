#!/usr/bin/python

from lxml import html
import json


def extract_item_info(item, item_types=[]):
    title = (item.xpath('.//p[@class="item-title"]/text()') or [""])[0]

    subtitle = (item.xpath('.//p[@class="pickup"]/text()') or [""])[0].replace("\"", "")

    description_parts = []
    description_lines = item.xpath(u'.//p[starts-with(text(), "\u2022")]/text()')
    for line in description_lines:
        splits = line.split("\n")
        rejoined = " ".join([split.replace(u"\u2022", "").strip() for split in splits])
        description_parts.append(rejoined) 

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
        "title": title,
        "subtitle": subtitle,
        "description_parts": description_parts,
        "item_pools": item_pools,
        "item_types": item_types,
        "search_tags": search_tags
    }
    return info

content = html.parse('platinumgod.co.uk/index.html')

item_containers = content.xpath('//div[contains(@class, "items-container")]')
trinket_containers = content.xpath('//div[contains(@class, "trinkets-container")]')
usable_containers = content.xpath('//div[contains(@class, "tarot-container")]')

infos = []
for item_container in item_containers:
    items = item_container.xpath('.//li[@class="textbox"]')
    for item in items:
        info = extract_item_info(item)
        infos.append(info)

for trinket_container in trinket_containers:
    items = trinket_container.xpath('.//li[@class="textbox"]')
    for item in items:
        info = extract_item_info(item, item_types=["Trinket"])
        infos.append(info)

for usable_container in usable_containers:
    items = usable_container.xpath('.//li[@class="textbox"]')
    for item in items:
        info = extract_item_info(item, item_types=["Usable"])
        infos.append(info)

with open("../data/items.json", "w") as f:
    json.dump(infos, f)
