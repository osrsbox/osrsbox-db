# osrsbox-db: Workflow tools

## DetermineNewItems.py

- This script takes two files as arguments
    - NEW JSON file from ItemScraper RuneLite plugin (`allitems.json`)
    - OLD JSON file from ItemScraper RuneLite plugin (`allitems.json`)
- A simple list is returned with
    - New items
    - Changed items
    - Removed items
- Only item name + item id is returned
- Good to determine new items added to game since last dump
- Command to run:
- `python3.6 DetermineNewItems.py -n allitems.json -o ../docs/allitems.json`
- `python.exe .\DetermineNewItems.py -n allitems.json -o ..\docs\allitems.json`

## JoinSingleJSONFiles.py

- This script takes a directory as an argument
- For example: The directory could be:
    - `..\docs\items-json`
    - `..\item_db_tools\items-json`
- The script will parse all single JSON files
- All JSON files are combined into allitems_db.json
- Command to run:
- `python3.6 JoinSingleJSONFiles.py -d ../docs/items-json`
- `python.exe JoinSingleJSONFiles.py -d ..\docs\items-json`

## CheckMissingItems.py

- Comparing existing osrsbox-db contents to new allitems.json
- Command input:
    - allitems.json file
    - allitems_db.json file (output of JoinSingleJSONFiles.py)
- A simple list is returned with new items
- Only item name + item id is returned
- Good to determine items missing from osrsbox-db
- Command to run:
- `python3.6 CheckMissingItems.py -f ../docs/allitems.json -d allitems_db.json`
- `python.exe .\CheckMissingItems.py -f ..\docs\allitems.json -d allitems_db.json`

## allitems_db.json

- osrsbox-db contents (items-json) amalgamated into one JSON file
- Created using JoinSingleJSONFiles.py

## osrsbox-db-missing-items.txt

- List of items currently missing from osrsbox-db
- Created using CheckMissingItems.py
- Contains: item-id,item-name