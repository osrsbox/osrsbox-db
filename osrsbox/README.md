# osrsbox-db 

[![Build Status](https://travis-ci.org/osrsbox/osrsbox-db.svg?branch=master)](https://travis-ci.org/osrsbox/osrsbox-db) [![PyPI version](https://badge.fury.io/py/osrsbox.svg)](https://badge.fury.io/py/osrsbox)

## A complete and up-to-date database of Old School Runescape (OSRS) items

The `osrsbox` package is a complete and up-to-date database of OSRS items that is accessible via a Python API. **Complete** means it holds every single items in OSRS. **Up-to-date** means this database is updated after every weekly game update to ensure accurate information. This package contains just the Python API and the actual item database - the tools and data used to build the item database are available from the [`osrsbox-db` GitHub repository](https://github.com/osrsbox/osrsbox-db).

### Quick Start

- Make sure you have >= Python 3.6
- Install package using: `pip install osrsbox`
- Import items API using: `from osrsbox import items_api`
- Load all items using: `all_db_items = items_api.load()`
- Loop items using: `for item in all_db_items: print(item.name)`

### Package Requirements

- Python 3.6 or above

### Installation

The easiest way to install the osrsbox package is through the [Python Package Index](http://pypi.python.org/) using the `pip` command. You need to have `pip` installed - and make sure it is updated (especially on Windows). Then you can install the `osrsbox` package using `pip`:

```
pip install osrsbox
```


Alternatively, you can clone the latest development release using `git` and install the package using the following commands:

```
git clone https://github.com/osrsbox/osrsbox-db.git
cd osrsbox-db
python setup.py install
```

### Usage 

The key use of the `osrsbox` package is to load and automate processing of OSRS items and their associated metadata. Each item is represented by the following objects:

- `ItemDefinition`: Contains basic item metadata such as `name`, `name`, `examine` text, store `cost`, `high_alch` and `low_alch` values and `quest` association.
- `ItemEquipment`: All equipable items (armour and weapons) have stats including `attack_slash`, `defence_crush` and `melee_strength` values. Additional information about equipable items include `skill_reqs` to wear armour or wield weapons, and `attack_speed` and item `slot` properties.

You can load the package using `import osrsbox`, however, you probably want to load the `items_api` module. A simple example of using the package to load all the items, then print out the item ID and name of every item in OSRS is provided below:

```
>>> from osrsbox import items_api
>>> all_db_items = items_api.load()
>>> for item in all_db_items:
...     print(item.id, item.name)
```
