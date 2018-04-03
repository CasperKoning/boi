import pydoc
import json as json_lib

formatter_names = ["json", "simple"]

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

formatters = {
    "json": json,
    "simple": simple
}
