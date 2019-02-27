# osrsbox-db 

[![Build Status](https://travis-ci.org/osrsbox/osrsbox-db.svg?branch=master)](https://travis-ci.org/osrsbox/osrsbox-db) [![PyPI version](https://badge.fury.io/py/osrsbox.svg)](https://badge.fury.io/py/osrsbox)

## A complete and up-to-date database of Old School Runescape (OSRS) items

This repository hosts a complete and up-to-date database of OSRS items. **Complete** means it holds every single items in OSRS. **Up-to-date** means this database is updated after every weekly game update to ensure accurate information. Current development is working towards adding a similar database for monsters.

## The `osrsbox` Package

If you just want to access the item database, it is probably more sensible to use the [`osrsbox` package available from PyPi](https://pypi.org/project/osrsbox/1.0.0/). This repo hosts the package in the `osrsbox` folder, while the other folders are used to store essential data and Python modules to build the item database. You can install the `osrsbox` package using `pip`:

```
pip install osrsbox
```

You can load the package using `import osrsbox`, however, you probably want to load the `items_api` module directly. A simple example of using the package to print out the name of every item in OSRS is provided below:

```
>>> from osrsbox import items_api
>>> all_db_items = items_api.load()
>>> for item in all_db_items:
...     print(item.id, item.name)
```

More information regarding loading and using the package can be found in the [`osrsbox` package README file](osrsbox/README.md). Additionally, for more additional information about the project see: 

- https://www.osrsbox.com/projects/osrsbox-db/
- https://www.osrsbox.com/blog/tags/Database/

## Summary of Project Structure

- `data`: Collection of useful data files used in the osrsbox-db project.
- `docs`: The publicly accessible item database available through this repo or a somewhat-RESTful API. This folder contains the actual item database that is publicly available, or browsable within this repository.
- `extraction_tools_cache`: An up-to-date OSRS cache dump (compressed) with associated tools used in other parts in this project.
- `extraction_tools_other`: Collection of Python tools to extract data from a variety of sources including equipable item skill requirements, grand exchange buy limits, and name normalization for more efficient OSRS Wiki lookups.
- `extraction_tools_wiki`: Collection of Python modules to extract data from the new (non-Wikia) OSRS Wiki site. There is also dumped data (category page titles and raw wiki text) for items, quests and monsters that is somewhat-regularly updated.
- `items_builder`: Collection of Python scripts to build the item database. The `builder.py` script is the primary entry point.
    - `update_tools`: Scripts used to update all data files after each weekly game update. 
- `osrsbox`: The future Python package:
    - `items_api`: The Python API for interacting with the items database. Has modules to load all items in the database, iterate through items and access the different item properties.
    - `items_tools`: A collection of simple Python scripts that use the `items_api` to provide an example of what can be achieved and how to use the items database.
- `test`: A collection of unit tests
- `CHANGELOG_items.md`: Document of items added, removed or changed in each weekly game update that have been added to the database.
 