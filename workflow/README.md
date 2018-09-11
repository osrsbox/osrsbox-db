# osrsbox-db workflow tools

## DetermineNewItems.py

- This script takes two files as arguments
    - NEW JSON file from ItemScraper RuneLite plugin (allitems.json)
    - OLD JSON file from ItemScraper RuneLite plugin (allitems.json)
- A simple list is returned with new items
- Only item name + item id is returned
- Good to determine new items added to game since last dump
- Command to run:
- `python3.6 DetermineNewItems.py -n allitems.json -o ../docs/allitems.json`
- `python.exe .\DetermineNewItems.py -n allitems.json -o ..\docs\allitems.json`

## JoinSingleJSONFiles.py

- This script takes a directory as an argument
- The directory should be docs/items-json 
- The script will parse all single JSON files
- All JSON files are combined into allitems_db.json
- Command to run:
- `python3.6 JoinSingleJSONFiles.py -d ../docs/items-json`
- `python.exe JoinSingleJSONFiles.py -d ..\docs\items-json`

## CheckMissingItems

- Comparing existing osrsbox-db contents to new allitems.json
- A simple list is returned with new items
- Only item name + item id is returned
- Good to determine items missing from osrsbox-db
- Command to run:
- `python3.6 CheckMissingItems.py -f ../docs/allitems.json -d ../docs/items-json/`
- `python.exe .\CheckMissingItems.py -f ..\docs\allitems.json -d ..\docs\items-json\`