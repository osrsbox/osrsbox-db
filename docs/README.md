## osrsbox-db: Public RESTful API docs/ Folder

This folder contains the publicly available database/dataset and somewhat-RESTful API of osrsbox-db. Basically, every file inside this specfic folder can be fetched using HTTP GET requests. The base URL for this folder is `https://www.osrsbox.com/osrsbox-db/`. Simply append any file name (from this folder) to the base URL, and you can fetch this data. You can also clone this entire repository and access the files provided in this folder.
 
A summary of the contents are listed below with descriptions:

- `items-icons`: Collection of PNG files (20K+) for every item inventory icon in OSRS
- `items-json`: Collection of JSON files (20K+) of extensive item metadata for every item in OSRS
- `items-json-slot`: Collection of JSON files extracted from the database that are specific for each equipment slot (e.g., head, legs)
- `items-complete.json`: A single JSON file that contains all single JSON files from `items-json`
- `items-scraper.json`: A single JSON file that contains raw item metadata from the OSRS cache (this file has less information than `items-complete.json` and no metadata from the OSRS Wiki)
- `items-summary.json`: A single JSON file that contains only item name and item ID number
- `models-summary.json`: A single JSON file that contains model ID numbers for items, objects and NPCs
