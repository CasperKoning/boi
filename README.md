# BOI
This is your command line interface into the Binding of Isaac.

## Installation
```bash
pip3 install -r requirements.txt
pip3 install -e .
```

## Usage
`boi` provides useful `--help` flags to help you discover the CLI by yourself:
```bash
boi --help

Usage: boi [OPTIONS] COMMAND [ARGS]...

  boi - Command line interface for discovering Binding of Isaac details

Options:
  --help  Show this message and exit.

Commands:
  item     Get details regarding items
  trinket  Get details regarding trinkets
```

### Formats
Most functions allow specifying different format via the `-f` or `--format` flags, e.g.
```bash
boi item id 10 --format=json
```
The supported formats are:
- `simple`: A simple tabular format listing all items.
- `page`: A detailed page on a single item, including its picture. Requires you to select a single item from a list if multiple items are returned from the CLI.
- `json`: JSON structure listing all items to easily be consumed by other applications.

## Examples
Some examples of commands you can run:

### Listing all items/trinkets
[![asciicast](https://asciinema.org/a/5nqAVhajSfgbuHks8FP7ycK3K.png)](https://asciinema.org/a/5nqAVhajSfgbuHks8FP7ycK3K)

For listing all items:
```bash
boi item all
```
or 
all trinkets:
```bash
boi trinket all
```

### Searching by name or subtitle
[![asciicast](https://asciinema.org/a/U0UvTwApV4s4Tjur06lUAjAI4.png)](https://asciinema.org/a/U0UvTwApV4s4Tjur06lUAjAI4)
You can search by name of the item
```bash
boi item search "Brimstone"
```
or it's subtitle
```bash
boi item search "not butter bean"
```

### Searching by item aspects
[![asciicast](https://asciinema.org/a/c3bN9RNB1Go2VZgaDO261Die5.png)](https://asciinema.org/a/c3bN9RNB1Go2VZgaDO261Die5)

Searching by certain aspects of the items are also possible (possible search terms have been shamelessly copied from [platinumgod](http://platinumgod.co.uk)), like color:
```bash
boi item search "pink"
```

## Acknowledgements
- [pokedex-cli](https://github.com/Tenchi2xh/pokedex-cli): A CLI Pokedex. This was the main inspiration (both in spirit and in code) for this project. 
- [platinumgod.co.uk](http://platinumgod.co.uk): Used for getting item descriptions and search tags, among others.
- [bindingofisaacrebirth.gamepedia.com](https://bindingofisaacrebirth.gamepedia.com/Binding_of_Isaac:_Rebirth_Wiki): For getting item information such as images.
