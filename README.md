# osrsbox-db

## A complete and up-to-date database of Old School Runescape (OSRS) items

This repopository hosts a complete and up-to-date database of OSRS items. Complete means it holds every single items in OSRS. Up-to-date means this database is updated after every weekly game update to ensure accurate information. 

For more user-firendly information see: 

- https://www.osrsbox.com/projects/osrsbox-db/
- https://www.osrsbox.com/blog/tags/Database/

## Summary of Project Structure

- `docs`: The publicly accessible item database API. This folder contains the actual item database that is publicaly available, or browsable within this repository.
- `extraction_tools_other`: Collection of Python tools to extract data from a variety of sources including equipable item skill requirements, grand exchange buy limits, and name normalization for more efficient OSRS Wiki lookups
- `extraction_tools_wiki`: Collection of Python tools to extract data from the new (non-Wikia) OSRS Wiki site. There is also dumped data that is somewhat-regularly update
- `item_api_tools`: Collection of Python tools for interacting with the database. With this code you can write simple Python scripts to process and analyse the database contents.
- `item_db_tools`: Collection of Python tools used to create the OSRS item database. This code is currently a mess!
- `model_db_tools`: Collection of Python tools to handle model ID number extraction.
- `quest_db_tools`: Collection of Python tools used to create the OSRS quest database (work in progress).
- `CHANGELOG.txt`: Document of changes to the item database, specifically, newly added items. More detailed changes can be seen by viewing the commit logs of this repository.

For additional information on each component of the project, I would recommend viewing the `README.md` file that is provided for every folder in the project.
