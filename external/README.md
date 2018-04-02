## External sources
In this directory, you'll find scripts for extracting game data from external websites that we reuse in this project. All credits for these sources go to their respective websites. 

We extract the following:
### platinumgod.co.uk
Extracts the following information from platinumgod.co.uk:
- Item ID
- Title
- Subtitle
- Description
- Item pool
- Item type
- Search tags

### bindingofisaacrebirth.gamepedia.com
Based on the item ID, the icon is extracted and saved as `${item_id}.png`.

## Extracting data
A python script (`extract.py`) is provided that can be used to extract the necessary sources in case you need to rerun the extraction (for example when an external website is updated):
```bash
pip3 install -r requirements.txt
python3 extract.py
```

(Note: only supports python3)
