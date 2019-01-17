# osrsbox-db: OSRS Wiki extraction tools

Collection of Python tools to extract data from the new (non-Wikia) OSRS Wiki site. There is also dumped data that is somewhat-regularly update

## General workflow for updating:

- Start by extracting names for OSRS Wiki pages that need to be extracted
    - `python.exe .\extract_all_items.py`
- Next, extract the Wikicode from all required pages
    - `python.exe .\extract_all_items_page_wikitext.py`
    - This queries a lot of pages, approximately 8,000
    - Should only be run when necessary
- Next, run the script to join the individual JSON files
    - `python.exe .\extract_all_items_page_wikitext_join.py`
    - This will create a file called `extract_all_items_page_wikitext.json`
    - This file is added to the repo, while the `extract_all_items_page_wikitext` folder is not. This approach is only to easily restart the extract wikitext script after connection timeouts etc.
- Next, extract the templates from the OSRS Wiki wikicode file
    - `python.exe .\extract_all_items_templates.py`
    - This saves a collection of files that only contain wiki templates
    - These files are used for ingestion into `..\item_db_tools\ProcessItems.py`

# GENERAL

## extract_all_categories.py

- Purpose: Determine wiki category names for other scripts
- This script takes no command line arguments
- The script prints the name of every category on the OSRS Wiki
- You could also get the pageid (if code edited)
- Save the output using redirection
- Command to run:
- `python3.6 extract_all_categories.py`
- `python.exe .\extract_all_categories.py`

# ITEMS

## extract_all_items.py

- Purpose: Extract page titles for items from the following categories:
    - Category:Items
    - Category:Construction
    - Category:Furniture
    - Category:Flatpacks
    - Category:Pets 
- This script outputs one (hardcoded) file:
    - `extract_all_items.txt`
- The extracted item page title can be appended to the OSRS Wiki URL to visit the page
- Command to run:
- `python3.6 extract_all_items.py`
- `python.exe .\extract_all_items.py`

## extract_all_items_page_wikitext.py

- Purpose: Extract complete wikitext from all input page titles for all items
- The script ingests one (hardcoded) file:
    - `extract_all_items.txt`
- The script outputs wikitext to one (hardcoded) directory:
    - `extract_all_items_page_wikitext`
    - Output file names are randomised 64 characters
    - Each output JSON file contains key of item name, that maps to value of wikitext
- Command to run:
- `python3.6 extract_all_items_page_wikitext.py`
- `python.exe extract_all_items_page_wikitext.py`

## extract_all_items_templates.py

- Purpose: extract templates from wikitext/wikicode for all input pages
- The script ingests one (hardcoded) directory of file:
    - `extract_all_items_templates`
    - The directory is the output from `extract_all_items_page_wikitext.py`
    - This directory is not provided in the repository
- The script outputs multiple (hardcoded) files:
    - `extract_all_items_templates_InfoboxItems.json`
    - `extract_all_items_templatess_InfoboxBonuses.json`
    - `extract_all_items_templates_InfoboxConstruction.json`
    - `extract_all_items_templates_InfoboxPet.json`
- Command to run:
- `python3.6 extract_all_items_templates.py`
- `python.exe .\extract_all_items_templates.py`

# QUESTS

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
- `python.exe .\extract_all_quests.py`

## extract_all_quests_page_wikitext.py

- NOTE: This is the best script to use, pull data once
- Purpose: extract complete wikitext/wikicode from all input pages
- This script takes no command line arguments
- The script ingests (hardcoded) two files:
    - `extract_all_quests.txt`
- The script outputs two (hardcoded) files:
    - `extract_all_quests_page_wikitext.json`
- The script prints the name of every quest on the OSRS Wiki (unless redirected)
- This item name can be appended to the OSRS Wiki base URL to use with the API
- Command to run:
- `python3.6 extract_all_quests_page_wikitext.py`
- `python.exe extract_all_quests_page_wikitext.py`

# BESTIARY

Coming soon
