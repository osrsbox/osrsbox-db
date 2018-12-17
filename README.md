# osrsbox-db

## A complete and up-to-date database of Old School Runescape (OSRS) items

This repopository hosts a complete and up-to-date database of OSRS items. Complete means it holds every single items in OSRS. Up-to-date means this database is updated after every weekly game update to ensure accurate information. 

For more user-firendly information see: 

- https://www.osrsbox.com/projects/osrsbox-db/

## Summary of Project Structure

- `docs`: The publicly accessible item database API. This folder contains the actual item database that is publicaly available, or browsable within this repository.
- `item-api_tools`: Collection of Python tools for interacting with the database. With this code you can write simple Python scripts to process and analyse the database contents.
- `item_db_tools`: Collection of Python tools used to create the OSRS item database. This code is currently a mess!
- `item_db_workflow`: Collection of Python tools to handle newly added OSRS items.
- `model_db_tools`: Collection of Python tools to handle model ID number extraction.
- `quest_db_tools`: Collection of Python tools used to create the OSRS quest database (work in progress).
- `wiki_extraction_tools`: Collection of Python tools to extract data from the OSRS Wiki site. There is also dumped data that is somewhat-regularly update
- `CHANGELOG.txt`: Document of changes to the item database, specifically, newly added items. More detailed changes can be seen by viewing the commit logs of this repository.
