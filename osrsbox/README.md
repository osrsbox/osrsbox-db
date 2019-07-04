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
- Dataclasses package (if Python is below 3.7)

### Installation

The easiest way to install the osrsbox package is through the [Python Package Index](http://pypi.python.org/) using the `pip` command. You need to have `pip` installed - and make sure it is updated (especially on Windows). Then you can install the `osrsbox` package using `pip`:

```
pip install osrsbox
```

This package is consistently updated - usually after each weekly in-game update. This is because the in-game update usually introduces additional items into the game or changes existing items. Therefore, you should regularly check and update the `osrsbox` package. To achieve this, run `pip` with the `upgrade` flag.

```
pip install --upgrade osrsbox
```

### Usage 

The key use of the `osrsbox` package is to load and automate the processing of OSRS items and their associated metadata. 

You can load the package using `import osrsbox`, however, you probably want to load the `items_api` module. A simple example of using the package to `load` all the items, then loop and print out the item ID and name of every item in OSRS is provided below:

```
>>> from osrsbox import items_api
>>> all_db_items = items_api.load()
>>> for item in all_db_items:
...     print(item.id, item.name)
```

### Item Classes

Each item is represented by Python objects, specifically using Python dataclasses. There are three types of objects that can be used to represent part of an in-game OSRS item:

- `ItemDefinition`: An item that is not equipable, and not a weapon. This object type includes basic item metadata such as `id`, `name`, `examine` text, store `cost`, `high_alch` and `low_alch` values and `quest` association. Every item object in the database has these properties.

- `ItemEquipment`: Many items in OSRS are equipable, this includes armour and other _wearable_ items. Any equipable item (that is not a weapon) is stored as an `ItemEquipment` object including attributes such as `attack_slash`, `defence_crush` and `melee_strength` values. Additional information about equipable items include skill `requirements` to wear armour or wield weapons, and item `slot` properties. Finally, every equipable item also has all the properties available in the `ItemDefinition` class.
  
- `ItemWeapon`: A selection of OSRS items are both equipable, and also weapons. The `ItemWeapon` class has additional weapon-specific attributes including `attack_speed` and `weapon_types`. Additionally, each weapon has an array of combat stances associated with it to determine the `combat_style`, `attack_type`, `attack_style` and any `bonuses` or combat `experience` association. Finally, every weapon item also has the properties available in the `ItemDefinition` and `ItemEquipment` classes. 

### Item Properties

Every item in the osrsbox-db project has a selection of mandatory properties. These mandaotry properties are represented in the `ItemDefinition` class - while the `ItemEquipment` and `ItemWeapon` classes also have these mandatory properties. Therefore, every item in the database has these properties. All of the properties available are listed in the table below including the property name, the data types used, a description of the property and if the property is required to be populated - if not required, the property value can potentially be set to `None`.

| Property            | Data type   | Description                                          | Required |
| ------------------- | ----------- | ---------------------------------------------------- | -------- |
| id                  | integer     | Unique OSRS item ID number                           | Yes      |
| name                | string      | Name of the item                                     | Yes      |
| members             | boolean     | If the item is a members-only item                   | Yes      |
| tradeable           | boolean     | If the item is tradeable (between players and GE)    | No       |
| tradeable_on_ge     | boolean     | If the item is tradeable (only on GE)                | Yes      |
| stackable           | boolean     | If the item is stackable (in inventory)              | Yes      |
| noted               | boolean     | If the item is noted                                 | Yes      |
| noteable            | boolean     | If the item is notable                               | Yes      |
| linked_id           | integer     | The noted/unnoted equivalent of the item             | No       |
| placeholder         | boolean     | If the item is a placeholder                         | Yes      |
| equipable           | boolean     | If the item is equipable (based on menu entry)       | Yes      |
| equipable_by_player | boolean     | If the item is equipable by a player                 | Yes      |
| equipable_weapon    | boolean     | If the item is an equipable weapon                   | Yes      |
| cost                | integer     | The store price of an item                           | Yes      |
| lowalch             | integer     | The low alchemy value of the item (cost * .4)        | Yes      |
| highalch            | integer     | The high alchemy value of the item (cost * .6)       | Yes      |
| weight              | float       | The weight (in kilograms) of the item                | No       |
| buy_limit           | integer     | The Grand Exchange buy limit of the item             | No       |
| quest_item          | boolean     | If the item is associated with a quest               | No       |
| release_date        | string      | Date the item was released                           | No       |
| examine             | string      | The examine text for the item                        | No       |
| url                 | string      | OSRS Wiki URL link                                   | No       |
| equipment           | object      | Object of item equipment properties (if equipable)   | No       |
| weapon              | object      | Object of item weapon properties (if a weapon)       | No       |

Not all items in OSRS are equipable. Only items with the `equipable_by_player` property set to `true` are actually equipable. The `equipable` property is similar, but this is the raw data extracted from the game cache - and can sometimes be incorrect (not actually equipable by a player). Any item that is deemed equipable by a player is stored in a `ItemEquipment` object, which has additional properties concerning equipable items, and also has all the mandatory properties specified in the `ItemDefinition` class.  All of the properties available for equipable items are listed in the table below including the property name, the data types used, a description of the property and if the property is required to be populated - if not required, the property value can potentially be set to `None`. 

| Property        | Data type | Description                              | Required |
| --------------- | --------- | ---------------------------------------- | -------- |
| attack_stab     | integer   | The stab attack bonus of the item        | Yes      |
| attack_slash    | integer   | The slash attack bonus of the item       | Yes      |
| attack_crush    | integer   | The crush attack bonus of the item       | Yes      |
| attack_magic    | integer   | The magic attack bonus of the item       | Yes      |
| attack_ranged   | integer   | The ranged attack bonus of the item      | Yes      |
| defence_stab    | integer   | The stab defence bonus of the item       | Yes      |
| defence_slash   | integer   | The slash defence bonus of the item      | Yes      |
| defence_crush   | integer   | The crush defence bonus of the item      | Yes      |
| defence_magic   | integer   | The magic defence bonus of the item      | Yes      |
| defence_ranged  | integer   | The ranged defence bonus of the item     | Yes      |
| melee_strength  | integer   | The melee strength bonus of the item     | Yes      |
| ranged_strength | integer   | The ranged strength bonus of the item    | Yes      |
| magic_damage    | integer   | The magic damage bonus of the item       | Yes      |
| prayer          | integer   | The prayer bonus of the item             | Yes      |
| slot            | string    | The item slot (e.g., head)               | Yes      |
| requirements    | object    | An object of requirements {skill: level} | Yes      |

The final list of properties are for equipable weapon items. Only items with the `equipable_weapon` property set to `true` are equipable, and also weapons. Any item that is deemed an equipable weapon is stored in an `ItemWeapon` object, which has additional properties concerning weapons, and also has all the mandatory properties specified in the `ItemDefinition` and `ItemEquipment` class.  All of the properties available for weapons are listed in the table below including the property name, the data types used, a description of the property and if the property is required to be populated - if not required, the property value can potentially be set to `None`. 

| Property        | Data type | Description                              | Required |
| --------------- | --------- | ---------------------------------------- | -------- |
| attack_speed    | integer   | The attack speed of a weapon             | Yes      |
| weapon_type     | string    | The weapon classification (e.g., axe)    | Yes      |
| stances         | object    | An array of weapon stance information    | Yes      |

## Changelog

- `1.1.15`: Release for game update : 2019/07/04.
- `1.1.14`: Release for game update : 2019/06/27.
- `1.1.13`: Release for game update : 2019/06/20.
- `1.1.12`: Release for game update : 2019/05/30.
- `1.1.11`: Release for game update 2019/06/06.
- `1.1.10`: Release for game update 2019/05/23.
- `1.1.9`: Release for game update 2019/05/16.
- `1.1.8`: Release for week 2019/05/09 (no actual game update).
- `1.1.7`: Release for game update 2019/05/02.
- `1.1.6`: Release for game update 2019/04/25, added ItemWeapon class.
- `1.1.5`: Release for game update 2019/04/18.
- `1.1.4`: Update for changes to new treasure trail items.
- `1.1.3`: Release for game update 2019/04/11.
- `1.1.2`: Converted ItemDefinition, ItemEquipment to dataclass.
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
