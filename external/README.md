## External sources
In this directory, you'll find sources from external websites that we reuse in this project. All the sources for a website is contained within a folder named after the external website. All credits for these sources go to their respective websites. 

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
pip install -r requirements.txt
python extract.py
```
