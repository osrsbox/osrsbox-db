# osrsbox-db: OSRS Wiki extraction tools

## General workflow for updating:

- Start by extracting names for OSRS Wiki pages that need to be extracted
    - `python.exe .\extract_all_items.py > .\extract_all_items.txt`
    - If on Windows, change `extract_all_items.txt` encoding from UTF16 to UTF8
    - `python.exe .\extract_all_other.py > .\extract_all_other.txt`
    - If on Windows, change `extract_all_items.txt` encoding from UTF16 to UTF8
- Next, extract the Wikicode from all required pages
    - `python.exe .\extract_all_items_page_wikitext.py`
    - This queries a lot of pages, approximately 7,000
    - Should only be run when necessary
- Next, extract the templates from the OSRS Wiki wikicode file
    - `python.exe .\extract_templates.py`
    - This saves a collection of files that only contain wiki templates
    - These files are used for ingestion into `item_db_tools\ProcessItems.py`

## extract_all_categories.py

- Purpose: Determine wiki category names for other scripts
- This script takes no command line arguments
- The script prints the name of every category on the OSRS Wiki
- You could also get the pageid (if code edited)
- Save the output using redirection
- Command to run:
- `python3.6 extract_all_categories.py`
- `python3.6 extract_all_categories.py > extract_all_categories.txt`
- `python.exe .\extract_all_categories.py`
- `python.exe .\extract_all_categories.py > .\extract_all_categories.txt`

## extract_all_items.py

- Purpose: Extract item names from "Category:Items" 
- This script takes no command line arguments
- This item name can be appended to the OSRS Wiki URL to visit the page
- Save the output using redirection
- Command to run:
- `python3.6 extract_all_items.py`
- `python3.6 extract_all_items.py > extract_all_items.txt`
- `python.exe .\extract_all_items.py`
- `python.exe .\extract_all_items.py > .\extract_all_items.txt`

## extract_all_items_page_wikitext.py

- NOTE: This is the best script to use, pull data once
- Purpose: extract complete wikitext/wikicode from all input pages
- This script takes no command line arguments
- The script ingests (hardcoded) two files:
    - `extract_all_items.txt`
    - `extract_all_other.txt`
- The script outputs two (hardcoded) files:
    - `extract_all_items_page_wikitext.txt`
    - `extract_all_items_page_wikitext_bonuses.txt`
- The script prints the name of every item on the OSRS Wiki (unless redirected)
- This item name can be appended to the OSRS Wiki base URL to use with the API
- Command to run:
- `python3.6 extract_all_items_page_wikitext.py`
- `python.exe extract_all_items_page_wikitext.py`

## extract_all_other.py

- Purpose: Extract item names from:
    - Category:Construction
    - Category:Furniture
    - Category:Flatpacks
    - Category:Pets
- This script takes no command line arguments
- This item name can be appended to the OSRS Wiki URL to visit the page
- Save the output using redirection
- Command to run:
- `python3.6 extract_all_other.py`
- `python3.6 extract_all_other.py > extract_all_other.txt`
- `python.exe .\extract_all_other.py`
- `python.exe .\extract_all_other.py > .\extract_all_other.txt`

## extract_all_quests.py

- Purpose: Extract item names from:
    - Category:Quests
    - Category:Miniquests
    - Category:Special_quests
- This script takes no command line arguments
- This item name can be appended to the OSRS Wiki URL to visit the page
- Save the output using redirection
- Command to run:
- `python3.6 extract_all_quests.py`
- `python3.6 extract_all_quests.py > extract_all_quests.txt`
- `python.exe .\extract_all_quests.py`
- `python.exe .\extract_all_quests.py > .\extract_all_quests.txt`

## extract_all_quests_page_wikitext.py

- NOTE: This is the best script to use, pull data once
- Purpose: extract complete wikitext/wikicode from all input pages
- This script takes no command line arguments
- The script ingests (hardcoded) two files:
    - `extract_all_quests.txt`
- The script outputs two (hardcoded) files:
    - `extract_all_quests_page_wikitext.txt`
- The script prints the name of every quest on the OSRS Wiki (unless redirected)
- This item name can be appended to the OSRS Wiki base URL to use with the API
- Command to run:
- `python3.6 extract_all_quests_page_wikitext.py`
- `python.exe extract_all_quests_page_wikitext.py`

## extract_templates_infobox.py

- Purpose: extract templates from wikitext/wikicode for all input pages
- The script ingests one (hardcoded) files:
    - `extract_all_items_page_wikitext.txt`
- The script outputs multiple (hardcoded) files:
    - `extract_templates_InfoboxItems.txt`
    - `extract_templates_InfoboxBonuses.txt`
    - `extract_templates_InfoboxConstruction.txt`
    - `extract_templates_InfoboxPet.txt`
- Command to run:
- `python3.6 extract_templates.py`
- `python.exe .\extract_templates.py`

## normalized_names.txt

- This document stores information about OSRS items that are not directly extractable from the OSRS Wiki. The purpose of the document is to aid item metadata extraction by normalizing item names
- The structure of the file is:
    - `itemID|itemName|normalizedName|statusCode`
    - `itemID` is directly from the OSRS client cache
    - `itemName` is directly from the OSRS client cache
    - `nomalizedName` is the itemName normalized for the OSRS Wiki
    - `statusCode` documents specific item scenarios
