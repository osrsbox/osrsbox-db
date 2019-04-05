# osrsbox

![PyPI - Python Version](https://img.shields.io/pypi/pyversions/osrsbox.svg) [![PyPI version](https://badge.fury.io/py/osrsbox.svg)](https://badge.fury.io/py/osrsbox) ![PyPI - Downloads](https://img.shields.io/pypi/dm/osrsbox.svg)

## A complete and up-to-date database of Old School Runescape (OSRS) items accessible using a Python API

The `osrsbox` package is a complete and up-to-date database of OSRS items that is accessible via a Python API. **Complete** means it holds every single item in OSRS. **Up-to-date** means this database is updated after every weekly game update to ensure accurate information. This package contains just the Python API and the actual item database - the tools and data used to build the item database are available from the [`osrsbox-db` GitHub repository](https://github.com/osrsbox/osrsbox-db).

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

This package is consistently updated - usually after each in-game update. This is because the in-game update usually introduces additional items into the game or change existing items. Therefore, you should regularly check and update the `osrsbox` package. To achieve this, run `pip` with the `upgrade` flag.

```
pip install --upgrade osrsbox
```

### Usage 

The key use of the `osrsbox` package is to load and automate the processing of OSRS items and their associated metadata. 

You can load the package using `import osrsbox`, however, you probably want to load the `items_api` module. A simple example of using the package to load all the items, then print out the item ID and name of every item in OSRS is provided below:

```
>>> from osrsbox import items_api
>>> all_db_items = items_api.load()
>>> for item in all_db_items:
...     print(item.id, item.name)
```

### Item Properties

Each item is represented by the following objects:

- `ItemDefinition`: Contains basic item metadata such as `id`, `name`, `examine` text, store `cost`, `high_alch` and `low_alch` values and `quest` association.
- `ItemEquipment`: All equipable items (armour and weapons) have stats including `attack_slash`, `defence_crush` and `melee_strength` values. Additional information about equipable items include `skill_reqs` to wear armour or wield weapons, and `attack_speed` and item `slot` properties.

Every item in the osrsbox-db project has a selection of mandatory properties. All of the properties are listed in the table below.

| Property            | Data type   | Description                                          |
| ------------------- | ------------| -----------------------------------------------------|
| id                  | integer     | Unique OSRS item ID number                           |
| name                | string      | Name of the item                                     |
| members             | boolean     | If the item is a members-only item                   |
| tradeable           | boolean     | If the item is tradeable (between players and GE)    |
| tradeable_on_ge     | boolean     | If the item is tradeable (only on GE)                |
| stackable           | boolean     | If the item is stackable (in inventory)              |
| noted               | boolean     | If the item is noted                                 |
| notable             | boolean     | If the item is notable                               |
| linked_id           | integer     | The noted/unnoted equivalent of the item             |
| placeholder         | boolean     | If the item is a placeholder                         |
| equipable           | boolean     | If the item is equipable (based on menu entry)       |
| equipable_by_player | boolean     | If the item is equipable by a player                 |
| cost                | integer     | The store price of an item                           |
| lowalch             | integer     | The low alchemy value of the item (cost * .4)        |
| highalch            | integer     | The high alchemy value of the item (cost * .6)       |
| weight              | float       | The weight (in kilograms) of the item                |
| buy_limit           | integer     | The Grand Exchange buy limit of the item             |
| quest_item          | boolean     | If the item is associated with a quest               |
| release_date        | string      | Date the item was released                           |
| examine             | string      | The examine text for the item                        |
| url                 | string      | OSRS Wiki URL link                                   |
| equipment           | object      | Object of item equipment properties (if equipable)   |

Not all items in OSRS are equipable. Only items with the `equipable_by_player` property set to `true` are actually equipable. The `equipable` property is similar, but this is the raw data extracted from the game cache - and can sometimes be incorrect (not actually equipable by a player). Any item that is deemed equipable by a player has the following properties.

| Property        | Data type | Description                              |
| --------------- | --------- | ---------------------------------------- |
| attack_stab     | integer   | The stab attack bonus of the item        |
| attack_slash    | integer   | The slash attack bonus of the item       |
| attack_crush    | integer   | The crush attack bonus of the item       |
| attack_magic    | integer   | The magic attack bonus of the item       |
| attack_ranged   | integer   | The ranged attack bonus of the item      |
| defence_stab    | integer   | The stab defence bonus of the item       |
| defence_slash   | integer   | The slash defence bonus of the item      |
| defence_crush   | integer   | The crush defence bonus of the item      |
| defence_magic   | integer   | The magic defence bonus of the item      |
| defence_ranged  | integer   | The ranged defence bonus of the item     |
| melee_strength  | integer   | The melee strength bonus of the item     |
| ranged_strength | integer   | The ranged strength bonus of the item    |
| magic_damage    | integer   | The magic damage bonus of the item       |
| prayer          | integer   | The prayer bonus of the item             |
| slot            | string    | The item slot (e.g., head)               |
| attack_speed    | integer   | The attack speed of an item              |
| requirements    | object    | An object of requirements {skill: level} |

## Changelog

- `1.1.1`: Release for game update 2019/04/04.
- `1.1.0`: Changed equipable item requirements to an object.
- `1.0.9`: Release for game update 2019/03/28.
- `1.0.8`: Fixed packaging issue.
- `1.0.7`: Updated project documentation.
- `1.0.6`: Fixed package install bug.
- `1.0.5`: Release for game update 2019/03/21.
- `1.0.4`: Configured Travis CI for automated deployment.
- `1.0.3`: Release for game update 2019/03/14.
- `1.0.2`: Release for game update 2019/03/07.
- `1.0.1`: Release for game update 2019/02/14.
- `1.0.0`: Initial release.
