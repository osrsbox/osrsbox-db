# osrsbox-db wikia extraction tools

## extract_all_categories.py

- This script takes no command line arguments
- The script prints the name of every category on the OSRS Wiki
- You could also get the pageid (if code edited)
- Command to run:
- `python3.6 extract_all_categories.py`
- `python.exe .\extract_all_categories.py`

## extract_all_items.py

- This script takes no command line arguments
- The script prints the name of every item on the OSRS Wiki
- This item name can be appended to the OSRS Wiki URL to visit the page
- Command to run:
- `python3.6 extract_all_items.py`
- `python.exe extract_all_items.py`

## extract_all_pages.py

- This script takes no command line arguments
- The script prints the title of every page on the OSRS Wiki
- WARNING: This script will take a long time, and waste Wikia bandwidth
- Command to run:
- `python3.6 extract_all_pages.py`
- `python.exe extract_all_pages.py`

## extract_all_quests.py

- This script takes no command line arguments
- The script prints the name of every quest on the OSRS Wiki
- This quest name can be appended to the OSRS Wiki URL to visit the page
- Command to run:
- `python3.6 extract_all_quests.py`
- `python.exe extract_all_quests.py`

## extract_buy_limits.py

- This script takes no command line arguments
- The script does two things:
    - Fetch every item in Category:Items
    - Scrape the webpage for the buy limit value
- The raw HTML has to be scraped, as the OSRS Wiki API does not provide access to the buy limit value
- The item name (OSRS Wiki name) and buy limit is returned
- Redirect to a file to save the output
- The current delimiter is a pipe (`|`)
- Command to run:
- `python3.6 extract_buy_limits.py`
- `python.exe extract_buy_limits.py`
