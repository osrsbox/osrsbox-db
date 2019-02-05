# osrsbox-db [![Build Status](https://travis-ci.org/osrsbox/osrsbox-db.svg?branch=master)](https://travis-ci.org/osrsbox/osrsbox-db)

## A complete and up-to-date database of Old School Runescape (OSRS) items

This repopository hosts a complete and up-to-date database of OSRS items. Complete means it holds every single items in OSRS. Up-to-date means this database is updated after every weekly game update to ensure accurate information. Current development is working towards adding a similar database for monsters and quests.

For more user-friendly information see: 

- https://www.osrsbox.com/projects/osrsbox-db/
- https://www.osrsbox.com/blog/tags/Database/

## Summary of Project Structure

- `docs`: The publicly accessible item database available through this repo or a somewhat-RESTful API. This folder contains the actual item database that is publicly available, or browsable within this repository.
- `extraction_tools_other`: Collection of Python tools to extract data from a variety of sources including equipable item skill requirements, grand exchange buy limits, and name normalization for more efficient OSRS Wiki lookups
- `extraction_tools_wiki`: Collection of Python modules to extract data from the new (non-Wikia) OSRS Wiki site. There is also dumped data that is somewhat-regularly updated
- `item_api_tools`: Collection of Python tools for interacting with the database. With this code you can write simple Python scripts to process and analyse the database contents.
- `item_db_tools`: Collection of Python tools used to create the OSRS item database. This code is currently a mess!
- `model_db_tools`: Collection of Python tools to handle model ID number extraction.
- `quest_db_tools`: Collection of Python tools used to create the OSRS quest database (work in progress).
- `CHANGELOG_items.md`: Document of items added, removed or changed in each weekly game update that have been added to the database.
