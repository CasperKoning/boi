from pick import pick

def select_item(items):
    title = "Please select your item"
    max_title_width = max([len(item["title"]) for item in items])
    options = ['{title:{width}}\t{subtitle}'.format(title=item["title"], width=max_title_width, subtitle=item["subtitle"]) for item in items]
    option, index = pick(options, title)
    return items[index]