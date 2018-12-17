# osrsbox-db: Public API docs/ Folder

This folder contains the publicly available API of osrsbox-db. Basically, every file inside this specfic folder can be fetched using HTTP GET requests. The base URL for this folder is `https://www.osrsbox.com/osrsbox-db/`. Simply append any file name (from this folder) to the base URL, and you can fetch this data. A summary of the contents are listed below with descriptions:

- `items-icons`: An icon image for every item in OSRS
- `items-json`: Collection of JSON files (20K+) of extensive item metadata for every item in OSRS
- `items_complete.json`: A single JSON file that contains all single JSON files from `items-json`
- `items_itemscraper.json`: A single JSON file that contains raw item metadata from the OSRS cache (this file has less information than `items_complete.json` and no metadata from the OSRS Wiki)
- `items_summary.json`: A single JSON file that contains only item name and item ID number
- `models_summary.json`: A single JSON file that contains model ID numbers for items, objects and NPCs
