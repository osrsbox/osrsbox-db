# osrsbox-db: Item Database API Tools

This folder hosts the code used to build the osrsbox-db. This process is fully automated, so that no additional modification of the output JSON files is required. _Warning:_ This code is currently is a mess! I would not recommend using it, and it needs a tidy up for anyone else but myself to use! But feel free to use it as a reference or to get an idea of how the database is populated.

## ProcessItems.py

- Purpose: Handle construction of raw item data + OSRS Wiki data to JSON files for each item
- This script takes one command line argument:
    - `-f items_itemscraper.json`: This file should be taken from the docs directory
- Requirements:
    - `mwparserfromhell`
    - `dateparser`
- This script does not download any information from the OSRS Wiki. Instead it processes a collection of previously downloaded files from the `wikia_extraction` folder. All of these values are hardcoded that map to the files produced by the OSRS Wiki extraction tools.
- Command to run:
- `python3.6 ProcessItems.py -f ../docs/items_itemscraper.json`
- `python.exe .\ProcessItems.py -f ..\docs\items_itemscraper.json`

## ItemDefinition.py

- Purpose: Class to handle construction of a single OSRS item
- Each item is build from:
    - The raw ItemDefinition data taken from the ItemScraper plugin using RuneLite
    - Data extracted from the OSRS Wiki
    - Both are handled by the `ProcessItems.py` script

## ItemBonuses.py

- Purpose: Class to handle construction of equipment bonuses for a single OSRS item
- Each item bonuses are only build for equipable items
- All data is sourced from OSRS Wiki files

## ItemEquipment.py

- Purpose: Class to handle construction of equipment metadata for a single OSRS item
- Each item equipment are only build for equipable items
- All data is sourced from OSRS Wiki files
