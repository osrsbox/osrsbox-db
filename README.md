# osrsbox-db 

[![Build Status](https://travis-ci.org/osrsbox/osrsbox-db.svg?branch=master)](https://travis-ci.org/osrsbox/osrsbox-db) ![PyPI - Python Version](https://img.shields.io/pypi/pyversions/osrsbox.svg) 

[![PyPI version](https://badge.fury.io/py/osrsbox.svg)](https://badge.fury.io/py/osrsbox) ![PyPI - Downloads](https://img.shields.io/pypi/dm/osrsbox.svg)

[![Discord Chat](https://img.shields.io/discord/598412106118987787.svg)](https://discord.gg/HFynKyr)

[![Donate](https://img.shields.io/badge/Donate-PayPal-green.svg)](https://www.paypal.com/cgi-bin/webscr?cmd=_s-xclick&hosted_button_id=9J44ADGJQ5BC6&source=url)

## A complete and up-to-date database of Old School Runescape (OSRS) items, monsters and prayers

This project hosts a complete and up-to-date database of every item, every monster and every prayer in OSRS. **Complete** means it holds every single item, monster and prayer in OSRS. **Up-to-date** means this database is updated after every weekly game update to ensure accurate information. 

The item database has extensive properties for each item: a total of 27 properties for every item, an additional 16 properties for equipable items, and an additional 3 properties for equipable weapons. These properties include the item ID and name, whether an item is tradeable, stackable, or equipable or if the item is members only or associated with a quest. For any equipable item, there are additional properties about combat stats the item has; for example, what slash attack bonus, magic defence bonus or prayer bonus that an item provides. For weapons, additional properties are added which include attack speed and combat stance/weapon type information.

The monster database also has extensive properties: a total of 44 unique properties for each monster, as well as an array of item drops for each monster that has 6 additional properties per item drop. The base properties include the monster ID, name, member status, and all monster combat stats. Additional properties include slayer-related properties, attack type, hit points and max hit. Each monster also has an associated array of drops which document the item ID, name, rarity, quantity, and any requirements to get the drop.

The prayer database documentes each prayer that available in-game and has detailed properties: a total of 8 properties for every prayer. The base properties include the prayer name, members status, description, requirements, and bonuses that it provides.

## Table of Contents

- [Project Summary](#project-summary)
- [The `osrsbox` Python PyPi Package](#the-osrsbox-python-pypi-package)
- [The osrsbox RESTful API](#the-osrsbox-restful-api)
- [The `osrsbox-db` GitHub Repository](#the-osrsbox-db-github-repository)
- [The Item Database](#the-item-database)
- [The Monster Database](#the-monster-database)
- [The Prayer Database](#the-prayer-database)
- [Additional Project Information](#additional-project-information)
    - [Project Feedback](#project-feedback)
    - [Project Contribution](#project-contribution)
    - [Project License](#project-license)
    - [Project Attribution](#project-attribution)

## Project Summary

The osrsbox-db project provides three primary data sources for:

1. **Items**
1. **Monsters**
1. **Prayers**

The osrsbox-db project and data is accessible using three primary methods:

1. [**The Python PyPi package**](https://pypi.org/project/osrsbox/)
1. [**The RESTful API**](https://github.com/osrsbox/osrsbox-api/)
1. [**The GitHub development repository**](https://github.com/osrsbox/osrsbox-db/)

## The `osrsbox` Python PyPi Package

If you want to access the item and monster database programmatically using Python, the simplest option is to use the [`osrsbox` package available from PyPi](https://pypi.org/project/osrsbox/). You can load the item and/or monster database and process item objects, monster objects, and their properties. 

### Package Quick Start

- Make sure you have >= Python 3.6
- Install package using: `pip install osrsbox`
- Item database quick start:
    - Import items API using: `from osrsbox import items_api`
    - Load all items using: `all_db_items = items_api.load()`
    - Loop items using: `for item in all_db_items: print(item.name)`
- Monster database quick start:
    - Import monsters API using: `from osrsbox import monsters_api`
    - Load all monsters using: `all_db_monsters = monsters_api.load()`
    - Loop monsters using: `for monster in all_db_monsters: print(monster.name)`
- Prayer database quick start:
    - Import prayers API using: `from osrsbox import prayers_api`
    - Load all prayers using: `all_db_prayers = prayers_api.load()`
    - Loop prayers using: `for prayer in all_db_prayers: print(prayer.name)`

### Package Requirements

For the `osrsbox` PyPi package you must meet the following requirements:

- Python 3.6 or above
- Pip package manager
- Dataclasses package (if Python is below 3.7)

If you are using Python 3.6, the `dataclasses` package will automatically be installed. If you are using Python 3.7 or above, the `dataclasses` package is part of the standard library and will not be installed automatically.

### Package Installation

The easiest way to install the osrsbox package is through the [Python Package Index](http://pypi.python.org/) using the `pip` command. You need to have `pip` installed - and make sure it is updated (especially on Windows). Then you can install the `osrsbox` package using the following `pip` command:

```
pip install osrsbox
```

### Package Upgrading

The package is consistently updated - usually after each weekly in-game update. This is because the in-game update usually introduces additional items into the game or changes existing items. Therefore, you should regularly check and update the `osrsbox` package. To achieve this, run `pip` with the `upgrade` flag, as demonstrated in the following command:

```
pip install --upgrade osrsbox
```

### Package Usage 

The key use of the `osrsbox` package is to load and automate the processing of OSRS items and their associated metadata. You can load the package using `import osrsbox`, however, you probably want to load the `items_api` module or `monsters_api` module. A simple example of using the package to `load` all the items, then loop and print out the item ID and name of every item in OSRS is provided below:

```
phoil@gilenor ~ $ python3.6
Python 3.6.8 (default, Jan 14 2019, 11:02:34) 
[GCC 8.0.1 20180414 (experimental) [trunk revision 259383]] on linux
Type "help", "copyright", "credits" or "license" for more information.
>>> from osrsbox import items_api
>>> all_db_items = items_api.load()
>>> for item in all_db_items:
...     print(item.id, item.name)
```

Instead of using the Python interpreter, you can also write a simple script and import the `osrsbox` Python package. An example script is provided below, this time for the `monsters_api`:

```
#!/usr/bin/python3

from osrsbox import monsters_api

all_db_monsters = monsters_api.load()
for monster in all_db_monsters:
    print(monster.id, monster.name)
```

If you would like to review additional examples of using the `osrsbox` Python API, have a look at the [`items_api_examples` folder](https://github.com/osrsbox/osrsbox-db/tree/master/osrsbox/items_api_examples) and [`monsters_api_examples` folder](https://github.com/osrsbox/osrsbox-db/tree/master/osrsbox/monsters_api_examples). There are a number of scripts available that provide examples of loading and processing data using the Python API. 

## The osrsbox RESTful API

The [official osrsbox-api GitHub repository](https://github.com/osrsbox/osrsbox-api) hosts the source code used for the RESTful API. The official `osrsbox-api` project is available from:

- [https://api.osrsbox.com](https://api.osrsbox.com)

Have a look at the [official `osrsbox-api` project README](https://github.com/osrsbox/osrsbox-api/blob/master/README.md) for more information on API endpoints, documentation, Swagger UI availability and examples of API queries.

## The `osrsbox-db` GitHub Repository 

The [official osrsbox-db GitHub repository](https://github.com/osrsbox/osrsbox-db) hosts the source code for the entire osrsbox-db project. The Python PyPi package is located in the `osrsbox` folder of the official development repository, while the other folders in this repository are used to store essential data and Python modules to build the item database. 

### Using the Development Repository

If using this repository (the development version), you will need to fulfil some specific requirements. This includes having the following tools available on your system:

- Python 3.6 or above
- Pip - the standard package manager for Python
- A selection of additional Python packages

As a short example, I configured my Ubuntu 18.04 system to run the development repository code using the following steps:

```
sudo apt update
sudo apt install python3-pip
```

These two commands will install the `pip3` command, allowing the installation of Python packages. Then you can use `pip3` to install additional packages. The development repository requires a variety of Python packages in addition to the mandatory `dataclasses` package. These package requirements are documented in the [`requirements.txt`](https://github.com/osrsbox/osrsbox-db/tree/master/requirements.txt) file. It is recommended to use the `venv` module to set up your environment, then install the specified requirements. As an example, the following workflow is provided for Linux-based environments (make sure `python3` is available first):

```
git clone --recursive https://github.com/osrsbox/osrsbox-db.git
cd osrsbox-db
python -m venv venv
source venv/bin/activate
pip3 install -r requirements.txt
```

When you have finished with working in the `osrsbox-db` repository, make sure to deactivate the current `venv` environment using:

```
deactivate
```

### Summary of Repository Structure

- `builders`: The builders are the code that performs automatic regeneration of the databases. These builders read in a variety of data and produce a JSON file for each item or monster.
    - `items`: The item database builder that uses a collection of Python scripts to build the item database. The `builder.py` script is the primary entry point, and the `build_item.py` module does the processing of each item.
    - `monsters`: The monster database builder that uses a collection of Python scripts to build the monster database. The `builder.py` script is the primary entry point, and the `build_monster.py` module does the processing of each monster. Additionally, the `drop_table.py` module contains a selection of hard-coded drop tables for the various OSRS Wiki drop table templates such as the rare, herb, seed, gem and catacombs drop tables.
- `changelog`: A collection of markdown files that document the changes to items, monsters and PyPi package releases.
- `data`: Collection of useful data files used in the osrsbox-db project.
    - `cache`: OSRS client cache dump (not present in repository due to size, but populated using the `scripts/cache` scripts).
    - `items`: Data used for item database generation.
    - `monsters`: Data used for monster database generation.
    - `schemas`: JSON schemas for the item and monster database, as well as schemas for item, npc and object definitions from cache data.
    - `wiki`: OSRS Wiki data dump including all item and monster page titles and page data.
- `docs`: The publicly accessible item database available through this repo or by using the static JSON API. This folder contains the actual item database that is publicly available, or browsable within this repository (see section above for more information).
- `osrsbox`: The Python PyPi package:
    - `items_api`: The Python API for interacting with the items database. The API has modules to load all items in the database, iterate through items, and access the different item properties.
    - `items_api_examples`: A collection of simple Python scripts that use the `items_api` to provide an example of what can be achieved and how to use the items database.
    - `monsters_api`: The Python API for interacting with the monster database. The API has modules to load all monsters in the database, iterate through items, and access different monster properties.
    - `monsters_api_examples`: A collection of simple Python scripts that use the `monsters_api` to provide an example of what can be achieved and how to use the monster's database.
- `scripts`: A collection of scripts (using Python and BASH) to help automate common tasks including dumping the OSRS cache, scraping the OSRS wiki, generating schemas, updating the databases, and inserting data into a MongoDB database.
    - `cache`: A collection of scripts to extract useful data from the OSRS cache item, npc and object definition files.
    - `items`: A collection of scripts to help process data for the item builder.
    - `mongodb`: A collection of scripts for creating and inserting data into the MongoDB database.
    - `schemas`: A collection of scripts for generating and parsing the JSON schemas used in this project.
    - `update`: A collection of scripts for automating the data collection and database regeneration.
    - `wiki`: A collection of scripts for automating data extraction from the OSRS Wiki using the MediaWiki API.
- `test`: A collection of PyTest tests.

### Item, Monster and Prayer Database Schemas

Technically, the `osrsbox-db` is not really a database - more specifically it should be called a data set. Anyway... the contents in the item/monster/prayer database need to adhere to a specified structure, as well as specified data types for each property. This is achieved (documented and tested) using the [Cerberus project](https://docs.python-cerberus.org/en/stable/). The Cerberus schema is useful to determine the properties that are available for each entity, and the types and requirements for each property, including:

- `type`: Specifies the data type (e.g., boolean, integer, string)
- `required`: If the property must be populated (true or false)
- `nullable`: If the property can be set to `null` or `None`

The Cerberus schemas are provided in a dedicated repository called [`osrsbox/schemas`](https://github.com/osrsbox/schemas), and implorted into this project as a submodule - this is because the schemas are used in other respositories and central management is required. The schemas are loaded into the `data/schemas` folder and includes:

1. [`schema-items.json`](https://github.com/osrsbox/schemas/blob/master/schema-items.json): This file defines the item schema, the defined properties, the property types, and some additional specifications including regex validation, and/or property type specification.
1. [`schema-monsters.json`](https://github.com/osrsbox/schemas/blob/master/schema-monsters.json): This file defines the monster schema, the defined properties, the property types, and some additional specifications including regex validation, and/or property type specification.
1. [`schema-prayers.json`](https://github.com/osrsbox/schemas/blob/master/schema-prayers.json): This file defines the prayer schema, the defined properties, the property types, and some additional specifications including regex validation, and/or property type specification.

All Cerberus schema files are authored using Cerberus version 1.3.2. This project uses the [`Cerberus` PyPi package](https://pypi.org/project/Cerberus/).

## The Item Database

Each item is represented by Python objects when using the PyPi `osrsbox` package, specifically using Python dataclass objects. Additionally, the data is accessible directly by parsing the raw JSON files. There are three types of objects, or classifications of data, that can be used to represent part of an in-game OSRS item, each outlined in the following subsections.

### Item Properties

An `ItemProperties` object type includes basic item metadata such as `id`, `name`, `examine` text, store `cost`, `highalch` and `lowalch` values and `quest_item` association. Every item object in the item database has all of these properties. If you are parsing the raw JSON files all of these properties are in the root of the JSON document - so they are not nested. All of the properties available are listed in the table below including the property name, the data types used, a description of the property, if the property is required to be populated, and if the property is nullable (able to be set to `null` or `None`).

| Property | Data type | Description | Required | Nullable |
| -------- | --------- | ----------- | -------- |----------|
| id | integer | Unique OSRS item ID number. | True | False |
| name | string | The name of the item. | True | False |
| incomplete | boolean | If the item has incomplete wiki data. | True | False |
| members | boolean | If the item is a members-only. | True | False |
| tradeable | boolean | If the item is tradeable (between players and on the GE). | True | False |
| tradeable_on_ge | boolean | If the item is tradeable (only on GE). | True | False |
| stackable | boolean | If the item is stackable (in inventory). | True | False |
| stacked | boolean | If the item is stacked. | True | False |
| noted | boolean | If the item is noted. | True | False |
| noteable | boolean | If the item is noteable. | True | False |
| linked_id_item | integer | The linked ID of the actual item (if noted/placeholder). | True | True |
| linked_id_noted | integer | The linked ID of an item in noted form. | True | True |
| linked_id_placeholder | integer | The linked ID of an item in placeholder form. | True | True |
| placeholder | boolean | If the item is a placeholder. | True | False |
| equipable | boolean | If the item is equipable (based on right-click menu entry). | True | False |
| equipable_by_player | boolean | If the item is equipable in-game by a player. | True | False |
| equipable_weapon | boolean | If the item is an equipable weapon. | True | False |
| cost | integer | The store price of an item. | True | False |
| lowalch | integer | The low alchemy value of the item (cost * 0.4). | True | False |
| highalch | integer | The high alchemy value of the item (cost * 0.6). | True | False |
| weight | float | The weight (in kilograms) of the item. | True | True |
| buy_limit | integer | The Grand Exchange buy limit of the item. | True | True |
| quest_item | boolean | If the item is associated with a quest. | True | False |
| release_date | string | Date the item was released (in ISO8601 format). | True | True |
| duplicate | boolean | If the item is a duplicate. | True | False |
| examine | string | The examine text for the item. | True | True |
| icon | string | The item icon (in base64 encoding). | True | False |
| wiki_name | string | The OSRS Wiki name for the item. | True | True |
| wiki_url | string | The OSRS Wiki URL (possibly including anchor link). | True | True |
| equipment | dict | The equipment bonuses of equipable armour/weapons. | True | True |
| weapon | dict | The weapon bonuses including attack speed, type and stance. | True | True |

### Item Equipment

Many items in OSRS are equipable, this includes armor, weapons, and other _wearable_ items. Any equipable item has additional properties stored as an `ItemEquipment` object type - including attributes such as `attack_slash`, `defence_crush` and `melee_strength` values. The `ItemEquipment` object is nested within an `ItemProperties`. If you are parsing the raw JSON files, this data is nested under the `equipment` key. It is very important to note that not all items in OSRS are equipable. Only items with the `equipable_by_player` property set to `true` are equipable. The `equipable` property is similar, but this is the raw data extracted from the game cache - and can sometimes be incorrect (not equipable by a player). All of the properties available for equipable items are listed in the table below including the property name, the data types used, a description of the property, if the property is required to be populated, and if the property is nullable (able to be set to `null` or `None`).

| Property | Data type | Description | Required | Nullable |
| -------- | --------- | ----------- | -------- |----------|
| attack_stab | integer | The attack stab bonus of the item. | True | False |
| attack_slash | integer | The attack slash bonus of the item. | True | False |
| attack_crush | integer | The attack crush bonus of the item. | True | False |
| attack_magic | integer | The attack magic bonus of the item. | True | False |
| attack_ranged | integer | The attack ranged bonus of the item. | True | False |
| defence_stab | integer | The defence stab bonus of the item. | True | False |
| defence_slash | integer | The defence slash bonus of the item. | True | False |
| defence_crush | integer | The defence crush bonus of the item. | True | False |
| defence_magic | integer | The defence magic bonus of the item. | True | False |
| defence_ranged | integer | The defence ranged bonus of the item. | True | False |
| melee_strength | integer | The melee strength bonus of the item. | True | False |
| ranged_strength | integer | The ranged strength bonus of the item. | True | False |
| magic_damage | integer | The magic damage bonus of the item. | True | False |
| prayer | integer | The prayer bonus of the item. | True | False |
| slot | string | The equipment slot associated with the item (e.g., head). | True | False |
| requirements | dict | An object of requirements {skill: level}. | True | True |

### Item Weapon

A select number of items in OSRS are equipable weapons. Any equipable item that is a weapon has additional properties stored as an `ItemWeapon` type object including attributes such as `attack_speed` and `weapon_types` values. Additionally, each weapon has an array of combat stances associated with it to determine the `combat_style`, `attack_type`, `attack_style` and any `bonuses` or combat `experience` association. The `ItemWeapon` object is nested within an `ItemProperties` object when using the Python API. If you are parsing the raw JSON files, this data is nested under the `weapon` key.  It is very important to note that not all items in OSRS are equipable weapons. Only items with the `equipable_weapon` property set to `true` are equipable. All of the properties available for equipable weapons are listed in the table below including the property name, the data types used, a description of the property, if the property is required to be populated, and if the property is nullable (able to be set to `null` or `None`).

| Property | Data type | Description | Required | Nullable |
| -------- | --------- | ----------- | -------- |----------|
| attack_speed | integer | The attack speed of a weapon (in game ticks). | True | False |
| weapon_type | string | The weapon classification (e.g., axe) | True | False |
| stances | list | An array of weapon stance information. | True | False |

### Item: Python Object Example

A description of the properties that each item in the database can have is useful, but sometimes it is simpler to provide an example. Below is a full example of an item as loaded in a Python object, specifically the _Abyssal whip_ item. Since this item is a type of equipment, there is an `EquipmentProperties` object nested with combat bonuses. Additionally, this item is also a weapon, so there is a `WeaponProperties` object with extra information. If the item was not equipable, the `EquipmentProperties` property would be `None` and the `equipable_by_player` would be `False`. If the item was not a weapon, the `WeaponProperties` key would be `None` and the `equipable_weapon` would be `False`.

```
ItemProperties(
    id=4151,
    name='Abyssal whip',
    incomplete=True,
    members=True,
    tradeable=True,
    tradeable_on_ge=True,
    stackable=False,
    noted=False,
    noteable=True,
    linked_id_item=None,
    linked_id_noted=4152,
    linked_id_placeholder=14032,
    placeholder=False,
    equipable=True,
    equipable_by_player=True,
    equipable_weapon=True,
    cost=120001,
    lowalch=48000,
    highalch=72000,
    weight=0.453,
    buy_limit=70,
    quest_item=False,
    release_date='2005-01-26',
    duplicate=False,
    examine='A weapon from the abyss.',
    wiki_name='Abyssal whip',
    wiki_url='https://oldschool.runescape.wiki/w/Abyssal_whip',
    equipment=ItemEquipment(
        attack_stab=0,
        attack_slash=82,
        attack_crush=0,
        attack_magic=0,
        attack_ranged=0,
        defence_stab=0,
        defence_slash=0,
        defence_crush=0,
        defence_magic=0,
        defence_ranged=0,
        melee_strength=82,
        ranged_strength=0,
        magic_damage=0,
        prayer=0,
        slot='weapon',
        requirements={'attack': 70}
    ),
    weapon=ItemWeapon(
        attack_speed=4,
        weapon_type='whips',
        stances=[
            {'combat_style': 'flick',
            'attack_type': 'slash',
            'attack_style': 'accurate',
            'experience': 'attack',
            'boosts': None},
            {'combat_style': 'lash',
            'attack_type': 'slash',
            'attack_style': 'controlled',
            'experience': 'shared',
            'boosts': None},
            {'combat_style': 'deflect',
            'attack_type': 'slash',
            'attack_style': 'defensive',
            'experience': 'defence',
            'boosts': None}
        ]
    )
)
```

### Item: JSON Example

A description of the properties that each item in the database can have is useful, but sometimes it is simpler to provide an example. Below is a full example of an item, specifically the _Abyssal whip_ item. Since this item is a type of equipment, there is an `equipment` key with combat bonuses. Additionally, this item is also a weapon, so there is a `weapon` key with extra information. If the item was not equipable, the `equipment` key would be `null` and the `equipable_by_player` would be `false`. If the item was not a weapon, the `weapon` key would be `null` and the `equipable_weapon` would be `false`.

```
{
    "id": 4151,
    "name": "Abyssal whip",
    "incomplete": true,
    "members": true,
    "tradeable": true,
    "tradeable_on_ge": true,
    "stackable": false,
    "noted": false,
    "noteable": true,
    "linked_id_item": null,
    "linked_id_noted": 4152,
    "linked_id_placeholder": 14032,
    "placeholder": false,
    "equipable": true,
    "equipable_by_player": true,
    "equipable_weapon": true,
    "cost": 120001,
    "lowalch": 48000,
    "highalch": 72000,
    "weight": 0.453,
    "buy_limit": 70,
    "quest_item": false,
    "release_date": "2005-01-26",
    "duplicate": false,
    "examine": "A weapon from the abyss.",
    "wiki_name": "Abyssal whip",
    "wiki_url": "https://oldschool.runescape.wiki/w/Abyssal_whip",
    "equipment": {
        "attack_stab": 0,
        "attack_slash": 82,
        "attack_crush": 0,
        "attack_magic": 0,
        "attack_ranged": 0,
        "defence_stab": 0,
        "defence_slash": 0,
        "defence_crush": 0,
        "defence_magic": 0,
        "defence_ranged": 0,
        "melee_strength": 82,
        "ranged_strength": 0,
        "magic_damage": 0,
        "prayer": 0,
        "slot": "weapon",
        "requirements": {
            "attack": 70
        }
    },
    "weapon": {
        "attack_speed": 4,
        "weapon_type": "whips",
        "stances": [
            {
                "combat_style": "flick",
                "attack_type": "slash",
                "attack_style": "accurate",
                "experience": "attack",
                "boosts": null
            },
            {
                "combat_style": "lash",
                "attack_type": "slash",
                "attack_style": "controlled",
                "experience": "shared",
                "boosts": null
            },
            {
                "combat_style": "deflect",
                "attack_type": "slash",
                "attack_style": "defensive",
                "experience": "defence",
                "boosts": null
            }
        ]
    }
}
```

## The Monster Database

Each monster is represented by Python objects when using the PyPi `osrsbox` package, specifically using Python dataclass objects. Additionally, the data is accessible directly by parsing the raw JSON files. There are two types of objects, or classifications of data, that can be used to represent part of an in-game OSRS monster, each outlined in the following subsections. 

### Monster Properties

A `MonsterProperties` object type includes basic monster metadata such as `id`, `name`, `examine` text, `combat_level`, `attack_speed` and `hitpoints` values and slayer association such as `slayer_masters` who give this monster as a task. Every monster object in the monster database has all of these properties. If you are parsing the raw JSON files all of these properties are in the root of the JSON document - so they are not nested. All of the properties available are listed in the table below including the property name, the data types used, a description of the property, if the property is required to be populated, and if the property is nullable (able to be set to `null` or `None`).

| Property | Data type | Description | Required | Nullable |
| -------- | --------- | ----------- | -------- |----------|
| id | integer | Unique OSRS item ID number. | True | False |
| name | string | The name of the monster. | True | False |
| incomplete | boolean | If the monster has incomplete wiki data. | True | False |
| members | boolean | If the monster is members only, or not. | True | False |
| release_date | string | The release date of the monster (in ISO8601 format). | True | True |
| combat_level | integer | The combat level of the monster. | True | False |
| size | integer | The size, in tiles, of the monster. | True | False |
| hitpoints | integer | The number of hitpoints a monster has. | True | False |
| max_hit | integer | The maximum hit of the monster. | True | False |
| attack_type | list | The attack style (melee, magic, range) of the monster. | True | False |
| attack_speed | integer | The attack speed (in game ticks) of the monster. | True | True |
| aggressive | boolean | If the monster is aggressive, or not. | True | False |
| poisonous | boolean | If the monster poisons, or not | True | False |
| immune_poison | boolean | If the monster is immune to poison, or not | True | False |
| immune_venom | boolean | If the monster is immune to venom, or not | True | False |
| weakness | list | An array of monster weaknesses. | True | False |
| category | list | An array of monster category. | True | False |
| slayer_monster | boolean | If the monster is a potential slayer task. | True | False |
| slayer_level | integer | The slayer level required to kill the monster. | True | True |
| slayer_xp | float | The slayer XP rewarded for a monster kill. | True | True |
| slayer_masters | list | The slayer XP rewarded for a monster kill. | True | True |
| duplicate | boolean | If the monster is a duplicate. | True | False |
| examine | string | The examine text of the monster. | True | False |
| wiki_name | string | The OSRS Wiki name for the monster. | True | False |
| wiki_url | string | The OSRS Wiki URL (possibly including anchor link). | True | False |
| attack_level | integer | The attack level of the monster. | True | False |
| strength_level | integer | The strength level of the monster. | True | False |
| defence_level | integer | The defence level of the monster. | True | False |
| magic_level | integer | The magic level of the monster. | True | False |
| ranged_level | integer | The ranged level of the monster. | True | False |
| attack_stab | integer | The attack stab bonus of the monster. | True | False |
| attack_slash | integer | The attack slash bonus of the monster. | True | False |
| attack_crush | integer | The attack crush bonus of the monster. | True | False |
| attack_magic | integer | The attack magic bonus of the monster. | True | False |
| attack_ranged | integer | The attack ranged bonus of the monster. | True | False |
| defence_stab | integer | The defence stab bonus of the monster. | True | False |
| defence_slash | integer | The defence slash bonus of the monster. | True | False |
| defence_crush | integer | The defence crush bonus of the monster. | True | False |
| defence_magic | integer | The defence magic bonus of the monster. | True | False |
| defence_ranged | integer | The defence ranged bonus of the monster. | True | False |
| attack_accuracy | integer | The attack accuracy bonus of the monster. | True | False |
| melee_strength | integer | The melee strength bonus of the monster. | True | False |
| ranged_strength | integer | The ranged strength bonus of the monster. | True | False |
| magic_damage | integer | The magic damage bonus of the monster. | True | False |
| drops | list | An array of monster drop objects. | True | True |

### Monster Drops

Most monsters in OSRS drop items when they have been defeated (killed). All monster drops are stored in the `drops` property in an array containing properties about the item drop. When using the PyPi `osrsbox` package, these drops are represented by a list of `MonsterDrops` object type. When parsing the raw JSON files, the drops are stored in an array, that are nested under the `drops` key. The data included with the monster drops are the item `id`, item `name`, the drop `rarity`, whether the drop is `noted` and any `drop_requirements`. All of the properties available for item drops are listed in the table below including the property name, the data types used, a description of the property, if the property is required to be populated, and if the property is nullable (able to be set to `null` or `None`).

| Property | Data type | Description | Required | Nullable |
| -------- | --------- | ----------- | -------- |----------|
| id | integer | The ID number of the item drop. | True | False |
| name | string | The name of the item drop. | True | False |
| members | boolean | If the drop is a members-only item. | True | False |
| quantity | string | The quantity of the item drop (integer, comma-separated or range). | True | True |
| noted | boolean | If the item drop is noted, or not. | True | False |
| rarity | float | The rarity of the item drop (as a float out of 1.0). | True | True |
| drop_requirements | string | If there are any requirements to getting the specific drop. | True | True |

### Monster: Python Object Example 

A description of the properties that each monster in the database can have is useful, but sometimes it is simpler to provide an example. Below is a full example of a monster, specifically the _Abyssal demon_ monster. Please note that the number of item `drops` key data has been reduced to make the data more readable.

```
MonsterProperties(
    id=415,
    name='Abyssal demon',
    incomplete=False,
    members=True,
    release_date='2005-01-26',
    combat_level=124,
    size=1,
    hitpoints=150,
    max_hit=8,
    attack_type=['stab'],
    attack_speed=4,
    aggressive=False,
    poisonous=False,
    immune_poison=False,
    immune_venom=False,
    weakness=['magic', 'demonbane'],
    category=['abyssal demon'],
    slayer_monster=True,
    slayer_level=85,
    slayer_xp=150.0,
    slayer_masters=['vannaka', 'chaeldar', 'konar', 'nieve', 'duradel'], 
    duplicate=False,
    examine='A denizen of the Abyss!',
    wiki_name='Abyssal demon (Standard)',
    wiki_url='https://oldschool.runescape.wiki/w/Abyssal_demon#Standard',
    attack_level=97,
    strength_level=67,
    defence_level=135,
    magic_level=1,
    ranged_level=1,
    attack_stab=0,
    attack_slash=0,
    attack_crush=0,
    attack_magic=0,
    attack_ranged=0,
    defence_stab=20,
    defence_slash=20,
    defence_crush=20,
    defence_magic=0,
    defence_ranged=20,
    attack_accuracy=0,
    melee_strength=0,
    ranged_strength=0,
    magic_damage=0,
    drops=[
        MonsterDrop(
            id=592,
            name='Ashes',
            members=True,
            quantity='1',
            noted=False,
            rarity=1.0,
            drop_requirements=None
        ),
        MonsterDrop(
            id=4151,
            name='Abyssal whip',
            members=True,
            quantity='1',
            noted=False,
            rarity=0.001953125,
            drop_requirements=None
        ),
        MonsterDrop(
            id=565,
            name='Blood rune',
            members=True,
            quantity='7',
            noted=False,
            rarity=0.03125,
            drop_requirements=None
        ),
        MonsterDrop(
            id=19683,
            name='Dark totem top',
            members=True,
            quantity='1',
            noted=False,
            rarity=0.002857142857142857,
            drop_requirements='catacombs'
        ),
        MonsterDrop(
            id=12073,
            name='Clue scroll (elite)',
            members=True,
            quantity='1',
            noted=False,
            rarity=0.0008333333333333334,
            drop_requirements=None
        )
    ]
)
```

### Monster: JSON Example

A description of the properties that each monster in the database can have is useful, but sometimes it is simpler to provide an example. Below is a full example of a monster, specifically the _Abyssal demon_ monster. Please note that the number of item `drops` key data has been reduced to make the data more readable.

```
{
    "id": 415,
    "name": "Abyssal demon",
    "incomplete": false,
    "members": true,
    "release_date": "2005-01-26",
    "combat_level": 124,
    "size": 1,
    "hitpoints": 150,
    "max_hit": 8,
    "attack_type": [
        "stab"
    ],
    "attack_speed": 4,
    "aggressive": false,
    "poisonous": false,
    "immune_poison": false,
    "immune_venom": false,
    "weakness": [
        "magic",
        "demonbane"
    ],
    "slayer_monster": true,
    "slayer_level": 85,
    "slayer_xp": 150.0,
    "slayer_masters": [
        "vannaka",
        "chaeldar",
        "konar",
        "nieve",
        "duradel"
    ],
    "duplicate": false,
    "examine": "A denizen of the Abyss!",
    "wiki_name": "Abyssal demon (Standard)",
    "wiki_url": "https://oldschool.runescape.wiki/w/Abyssal_demon#Standard",
    "attack_level": 97,
    "strength_level": 67,
    "defence_level": 135,
    "magic_level": 1,
    "ranged_level": 1,
    "attack_stab": 0,
    "attack_slash": 0,
    "attack_crush": 0,
    "attack_magic": 0,
    "attack_ranged": 0,
    "defence_stab": 20,
    "defence_slash": 20,
    "defence_crush": 20,
    "defence_magic": 0,
    "defence_ranged": 20,
    "attack_accuracy": 0,
    "melee_strength": 0,
    "ranged_strength": 0,
    "magic_damage": 0,
    "drops": [
        {
            "id": 592,
            "name": "Ashes",
            "members": True,
            "quantity": "1",
            "noted": false,
            "rarity": "1.0",
            "drop_requirements": null
        },
        {
            "id": 4151,
            "name": "Abyssal whip",
            "members": true,
            "quantity": "1",
            "noted": false,
            "rarity": 0.001953125,
            "drop_requirements": null
        },
        {
            "id": 565,
            "name": "Blood rune",
            "members": true,
            "quantity": "7",
            "noted": false,
            "rarity": 0.03125,
            "drop_requirements": null
        },
        {
            "id": 19683,
            "name": "Dark totem top",
            "members": true,
            "quantity": "1",
            "noted": false,
            "rarity": 0.002857142857142857,
            "drop_requirements": "catacombs"
        },
        {
            "id": 12073,
            "name": "Clue scroll (elite)",
            "members": true,
            "quantity": "1",
            "noted": false,
            "rarity": 0.0008333333333333334,
            "drop_requirements": null
        }
    ]
}
```

## The Prayer Database

Each prayer is represented by Python objects when using the PyPi `osrsbox` package, specifically using Python dataclass objects Additionally, the data is accessible directly by parsing the raw JSON files. All prayer data is stored in a single object to represent the properties of an in-game OSRS prayer, which is outlined in the following subsection. 

### Prayer Properties

A `PrayerProperties` object type includes basic prayer metadata such as `id`, `name`, `description` text, `drain_per_minute`, `requirements` and `bonuses` values. Every prayer object in the prayer database has all of these properties. If you are parsing the raw JSON files all of these properties are in the root of the JSON document - so they are not nested. All of the properties available are listed in the table below including the property name, the data types used, a description of the property, if the property is required to be populated, and if the property is nullable (able to be set to `null` or `None`).

| Property | Data type | Description | Required | Nullable |
| -------- | --------- | ----------- | -------- |----------|
| id | integer | Unique prayer ID number. | True | False |
| name | string | The name of the prayer. | True | False |
| members | boolean | If the prayer is members-only. | True | False |
| description | string | The prayer description (as show in-game). | True | False |
| drain_per_minute | float | The prayer point drain rate per minute. | True | False |
| wiki_url | string | The OSRS Wiki URL. | True | False |
| requirements | dict | The stat requirements to use the prayer. | True | False |
| bonuses | dict | The bonuses a prayer provides. | True | False |

### Prayer: Python Object Example 

A description of the properties that each prayer in the database can have is useful, but sometimes it is simpler to provide an example. Below is a full example of a prayer, specifically the _Rigour_ prayer, as loaded in the `osrsbox` PyPi Python package.

```
PrayerProperties(
    id=28,
    name='Rigour',
    members=True,
    description='Increases your Ranged attack by 20% and damage by 23%,and your defence by 25%.',
    drain_per_minute=40.0,
    wiki_url='https://oldschool.runescape.wiki/w/Rigour',
    requirements={'prayer': 74, 'defence': 70}, 
    bonuses={'ranged': 20, 'ranged_strength': 25, 'defence': 23})
```

### Prayer: JSON Example

A description of the properties that each prayer in the database can have is useful, but sometimes it is simpler to provide an example. Below is a full example of a prayer, specifically the _Rigour_ prayer, as a JSON object.

```
{
    "id": 28,
    "name": "Rigour",
    "members": true,
    "description": "Increases your Ranged attack by 20% and damage by 23%, and your defence by 25%.",
    "drain_per_minute": 40.0,
    "wiki_url": "https://oldschool.runescape.wiki/w/Rigour",
    "requirements": {
        "prayer": 74,
        "defence": 70
    },
    "bonuses": {
        "ranged": 20,
        "ranged_strength": 25,
        "defence": 23
    }
}
```

## Additional Project Information

This section contains additional information about the osrsbox-db project. For detailed information about the project see the [`osrsbox.com`](https://www.osrsbox.com/) website for the official project page, and the _Database_ tag to find blog posts about the project: 

- https://www.osrsbox.com/projects/osrsbox-db/
- https://www.osrsbox.com/blog/tags/Database/

### Project Feedback

I would thoroughly appreciate any feedback regarding the osrsbox-db project, especially problems with the inaccuracies of the data provided. So if you notice any problem with the accuracy of item property data, could you please let me know. The same goes for any discovered bugs, or if you have a specific feature request. The best method is to [open a new Github issue](https://github.com/osrsbox/osrsbox-db/issues) in the project repository. 

### Project Contribution

This project would thoroughly benefit from a contribution from additional developers. Please feel free to submit a pull request if you have code that you wish to contribute - I would thoroughly appreciate the helping hand. For any code contributions, the best method is to [open a new GitHub pull request](https://github.com/osrsbox/osrsbox-db/pulls) in the project repository. Also, feel free to contact me (e.g., email) if you wish to discuss contribution before making a pull request. If you are not a software developer and want to contribute, even something as small as _Staring_ this repository really makes my day and keeps me motivated!

### Project License

The osrsbox-db project is released under the GNU General Public License version 3 as published by the Free Software Foundation. You can read the [LICENSE](LICENSE) file for the full license, check the [GNU GPL](https://www.gnu.org/licenses/gpl-3.0.en.html) page for additional information, or check the [tl;drLegal](https://tldrlegal.com/license/gnu-general-public-license-v3-(gpl-3)) documentation for the license explained in simple English. The GPL license is specified for all source code contained in this project. Other content is specified under GPL if not listed in the **Exceptions to GPL** below.

#### Exceptions to GPL

Old School RuneScape (OSRS) content and materials are trademarks and copyrights of JaGeX or its licensors. All rights reserved. OSRSBox and the osrsbox-db project is not associated or affiliated with JaGeX or its licensors. 

Additional data to help build this project is sourced from the [OSRS Wiki](https://oldschool.runescape.wiki/). This primarily includes item and monster metadata that is not available in the OSRS cache. As specified by the [Weird Gloop Copyright](https://meta.weirdgloop.org/w/Meta:Copyrights) page, this content is licensed under CC BY-NC-SA 3.0 - [Attribution-NonCommercial-ShareAlike 3.0 Unported](https://creativecommons.org/licenses/by-nc-sa/3.0/) license.

### Project Attribution

The osrsbox-db project is a labor of love. I put a huge amount of time and effort into the project, and I want people to use it. That is the entire reason for its existence. I am not too fussed about attribution guidelines... but if you want to use the project please adhere to the licenses used. Please feel free to link to this repository or my [OSRSBox website](https://www.osrsbox.com/) if you use it in your project - mainly so others can find it, and hopefully use it too!
