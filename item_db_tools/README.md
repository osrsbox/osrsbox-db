# osrsbox-db: Item database population tools

## ProcessItems.py

- Purpose: Handle construction of raw item data + OSRS Wiki data to JSON files for each item
- This script takes one command line argument:
    - `-f allitems.json`: This file should be taken from the docs directory
- Requirements:
    - `mwparserfromhell`
    - `dateparser`
- This script does not download any information from the OSRS Wiki. Instead it processes a collection of previously downloaded files from the `wikia_extraction` folder. All of these values are hardcoded that map to the files produced by the OSRS Wiki extraction tools.
- Command to run:
- `python3.6 ProcessItems.py`
- `python.exe .\ProcessItems.py`

## ItemDefinition.py

- Purpose: Handle construction of a single OSRS item
- Each item is build from:
    - The raw ItemDefinition data taken from the ItemScraper plugin using RuneLite
    - Data extracted from the OSRS Wiki
    - Both are handled by the `ProcessItems.py` script

## ItemBonuses.py

- Purpose: Handle construction of equipment bonuses for a single OSRS item
- Each item bonuses are only build for equipable items
- All data is sourced from OSRS Wiki files
