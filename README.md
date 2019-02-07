# osrsbox-db [![Build Status](https://travis-ci.org/osrsbox/osrsbox-db.svg?branch=master)](https://travis-ci.org/osrsbox/osrsbox-db)

## A complete and up-to-date database of Old School Runescape (OSRS) items

This repository hosts a complete and up-to-date database of OSRS items. Complete means it holds every single items in OSRS. Up-to-date means this database is updated after every weekly game update to ensure accurate information. Current development is working towards adding a similar database for monsters and quests.

For more user-friendly information see: 

- https://www.osrsbox.com/projects/osrsbox-db/
- https://www.osrsbox.com/blog/tags/Database/

## Summary of Project Structure

- `docs`: The publicly accessible item database available through this repo or a somewhat-RESTful API. This folder contains the actual item database that is publicly available, or browsable within this repository.
- `extraction_tools_other`: Collection of Python tools to extract data from a variety of sources including equipable item skill requirements, grand exchange buy limits, and name normalization for more efficient OSRS Wiki lookups
- `extraction_tools_wiki`: Collection of Python modules to extract data from the new (non-Wikia) OSRS Wiki site. There is also dumped data that is somewhat-regularly updated
- `CHANGELOG_items.md`: Document of items added, removed or changed in each weekly game update that have been added to the database.

## Current Project Status

The project is currently in an active stage of development with lots of changes happening. However, the items database is still current as of 2019/02/07. Although the items Python API has been temporarily removed, you can expect it back ASAP. The project is currently being re-structured and re-packaged into a much more logical manner. 
 