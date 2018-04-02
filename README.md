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

## Examples
Some examples of commands you can run:

### Listing all items/trinkets
For listing all items:
```bash
boi item all
```
or 
all trinkets:
```bash
boi trinket all
```

### Searching
You can search by name of the item
```bash
boi item search "Brimstone"
```
it's subtitle
```bash
boi item search "not butter bean"
```
or certain aspects of the items (possible search terms have been shamelessly copied from [platinumgod](http://platinumgod.co.uk)), like color:
```bash
boi item search "pink"
```
