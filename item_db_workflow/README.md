# osrsbox-db: Workflow tools

## DetermineNewItems.py

- This script takes two files as arguments
    - NEW JSON file from ItemScraper RuneLite plugin (`items_itemscraper.json`)
    - OLD JSON file from ItemScraper RuneLite plugin (`items_itemscraper.json`)
- A simple list is returned with
    - New items
    - Changed items
    - Removed items
- Only item name + item id is returned
- Good to determine new items added to game since last dump
- Command to run:
- `python3.6 DetermineNewItems.py -n items_itemscraper.json -o ../docs/items_itemscraper.json`
- `python.exe .\DetermineNewItems.py -n items_itemscraper.json -o ..\docs\items_itemscraper.json`

## JoinSingleJSONFiles.py

- This script takes a directory as an argument and a filename to output
- For example: The directory could be:
    - `..\docs\items-json`
    - `..\item_db_tools\items-json`
- The script will parse all single JSON files
- All JSON files are combined into allitems_db.json
- Command to run:
- `python3.6 JoinSingleJSONFiles.py -d ../docs/items-json -o output.json`
- `python.exe JoinSingleJSONFiles.py -d ..\docs\items-json -o output.json`

## CheckMissingItems.py

- Comparing existing osrsbox-db contents to new items_itemscraper.json
- Command input:
    - items_itemscraper.json file
    - allitems_db.json file (output of JoinSingleJSONFiles.py)
- A simple list is returned with new items
- Only item name + item id is returned
- Good to determine items missing from osrsbox-db
- Command to run:
- `python3.6 CheckMissingItems.py -f ../docs/items_itemscraper.json -d allitems_db.json`
- `python.exe .\CheckMissingItems.py -f ..\docs\items_itemscraper.json -d allitems_db.json`

## JoinSingleJSONFiles_ItemScraper.py

- This script is almost the same as `JoinSingleJSONFiles.py`, however, it sets the itemscraper plugin default for all properties scraped from the OSRS Wiki
- This script takes a directory as an argument and a filename to output
- For example: The directory could be:
    - `..\docs\items-json`
    - `..\item_db_tools\items-json`
- The script will parse all single JSON files
- All JSON files are combined into allitems_db.json
- Command to run:
- `python3.6 JoinSingleJSONFiles.py -d ../docs/items-json -o output.json`
- `python.exe JoinSingleJSONFiles.py -d ..\docs\items-json -o output.json`

## osrsbox-db-errors.txt

- List of items currently missing or incorrect from osrsbox-db
- Created using CheckMissingItems.py
