# osrsbox-db 

[![Build Status](https://travis-ci.org/osrsbox/osrsbox-db.svg?branch=master)](https://travis-ci.org/osrsbox/osrsbox-db) ![PyPI - Python Version](https://img.shields.io/pypi/pyversions/osrsbox.svg) 

[![PyPI version](https://badge.fury.io/py/osrsbox.svg)](https://badge.fury.io/py/osrsbox) ![PyPI - Downloads](https://img.shields.io/pypi/dm/osrsbox.svg)

## A complete and up-to-date database of Old School Runescape (OSRS) items and monsters

This project hosts a complete and up-to-date database of every item and every monster in OSRS. **Complete** means it holds every single item and monster in OSRS. **Up-to-date** means this database is updated after every weekly game update to ensure accurate information. 

The item database has extensive properties for each item: a total of 27 properties for every item, an additional 16 properties for equipable items, and an additional 3 properties for equipable weapons. These properties include the item ID and name, whether an item is tradeable, stackable, or equipable or if the item is members only or associated with a quest. For any equipable item, there are additional properties about combat stats the item has; for example, what slash attack bonus, magic defence bonus or prayer bonus that an item provides. For weapons, additional properties are added which include attack speed and combat stance/weapon type information.

The monster database also has extensive properties: a total of 44 unique properties for each monster, as well as an array of item drops for each monster that has 6 additional properties per item drop. The base properties include the monster ID, name, member status, and all monster combat stats. Additional properties include slayer-related properties, attack type, hit points and max hit. Each monster also has an associated array of drops which document the item ID, name, rarity, quantity, and any requirements to get the drop.

## Table of Contents

- [Project Summary](#project-summary)
- [The Item Database](#the-item-database)
- [The Monster Database](#the-monster-database)
- [The `osrsbox` Python PyPi Package](#the-osrsbox-python-pypi-package)
- [The `osrsbox-db` Static JSON API](#the-osrsbox-db-static-json-api)
- [The `osrsbox-db` GitHub Repository](#the-osrsbox-db-github-repository)
- [Additional Project Information](#additional-project-information)
    - [Project Feedback](#project-feedback)
    - [Project Contribution](#project-contribution)
    - [Project License](#project-license)
    - [Project Attribution](#project-attribution)

## Project Summary

The osrsbox-db project provides two primary data sources for:

1. **Items**
1. **Monsters**

The osrsbox-db project code and data is accessible using three primary methods:

1. [**The Python PyPi package named `osrsbox`**](https://pypi.org/project/osrsbox/)
1. [**The web-accessible, static JSON API**](https://github.com/osrsbox/osrsbox-db/tree/master/docs)
1. [**The GitHub repository for development**](https://github.com/osrsbox)

## The Item Database

Each item is represented by Python objects when using the PyPi `osrsbox` package, specifically using Python dataclass objects. Additionally, the data is accessible directly by parsing the raw JSON files. There are three types of objects, or classifications of data, that can be used to represent part of an in-game OSRS item, each outlined in the following subsections.

### Item Definition

An `ItemDefinition` object type includes basic item metadata such as `id`, `name`, `examine` text, store `cost`, `high_alch` and `low_alch` values and `quest_item` association. Every item object in the item database has all of these properties. If you are parsing the raw JSON files all of these properties are in the root of the JSON document - so they are not nested. All of the properties available are listed in the table below including the property name, the data types used, a description of the property and if the property is required to be populated - if not required, the property value can potentially be set to `None`.

| Property | Data type | Description | Required |
| -------- | --------- | ----------- | -------- |
| id | integer | Unique OSRS item ID number. | Yes |
| name | string | Name of the item. | Yes |
| members | boolean | If the item is a members-only. | Yes |
| tradeable | boolean | If the item is tradeable (between players and on the GE). | Yes |
| tradeable_on_ge | boolean | If the item is tradeable (only on GE). | Yes |
| stackable | boolean | If the item is stackable (in inventory). | Yes |
| noted | boolean | If the item is noted. | Yes |
| noteable | boolean | If the item is noteable. | Yes |
| linked_id_item | integer | The linked ID of the actual item (if noted/placeholder). | No |
| linked_id_noted | integer | The linked ID of an item in noted form. | No |
| linked_id_placeholder | integer | The linked ID of an item in placeholder form. | No |
| placeholder | boolean | If the item is a placeholder. | Yes |
| equipable | boolean | If the item is equipable (based on right-click menu entry). | Yes |
| equipable_by_player | boolean | If the item is equipable by a player and is equipable in-game. | Yes |
| cost | integer | The store price of an item. | Yes |
| lowalch | integer | The low alchemy value of the item (cost * 0.4). | Yes |
| highalch | integer | The high alchemy value of the item (cost * 0.6). | Yes |
| weight | number | The weight (in kilograms) of the item. | No |
| buy_limit | integer | The GE buy limit of the item. | No |
| quest_item | boolean | If the item is associated with a quest. | Yes |
| release_date | string | Date the item was released (in ISO8601 format). | No |
| duplicate | boolean | If the item is a duplicate. | Yes |
| examine | string | The examine text for the item. | No |
| wiki_name | string | The OSRS Wiki name for the item. | No |
| wiki_url | string | The OSRS Wiki URL (possibly including anchor link). | No |
| equipment | object | The equipment bonuses of equipable armour/weapons. | No |
| weapon | object | The information about weapon properties. | No |

### Item Equipment

Many items in OSRS are equipable, this includes armor, weapons, and other _wearable_ items. Any equipable item has additional properties stored as an `ItemEquipment` object type - including attributes such as `attack_slash`, `defence_crush` and `melee_strength` values. The `ItemEquipment` object is nested within an `ItemDefinition`. If you are parsing the raw JSON files, this data is nested under the `equipment` key. It is very important to note that not all items in OSRS are equipable. Only items with the `equipable_by_player` property set to `true` are equipable. The `equipable` property is similar, but this is the raw data extracted from the game cache - and can sometimes be incorrect (not equipable by a player). All of the properties available for equipable items are listed in the table below including the property name, the data types used, a description of the property and if the property is required to be populated - if not required, the property value can potentially be set to `None`.

| Property | Data type | Description | Required |
| -------- | --------- | ----------- | -------- |
| attack_stab | integer | The attack stab bonus of the item. | Yes |
| attack_slash | integer | The attack slash bonus of the item. | Yes |
| attack_crush | integer | The attack crush bonus of the item. | Yes |
| attack_magic | integer | The attack magic bonus of the item. | Yes |
| attack_ranged | integer | The attack ranged bonus of the item. | Yes |
| defence_stab | integer | The defence stab bonus of the item. | Yes |
| defence_slash | integer | The defence slash bonus of the item. | Yes |
| defence_crush | integer | The defence crush bonus of the item. | Yes |
| defence_magic | integer | The defence magic bonus of the item. | Yes |
| defence_ranged | integer | The defence ranged bonus of the item. | Yes |
| melee_strength | integer | The melee strength bonus of the item. | Yes |
| ranged_strength | integer | The ranged strength bonus of the item. | Yes |
| magic_damage | integer | The magic damage bonus of the item. | Yes |
| prayer | integer | The prayer bonus of the item. | Yes |
| slot | string | The equipment slot associated with the item (e.g., head). | Yes |
| requirements | object, null | An object of requirements {skill: level}. | Yes |

### Item Weapon

A select number of items in OSRS are equipable weapons. Any equipable item that is a weapon has additional properties stored as an `ItemWeapon` type object including attributes such as `attack_speed` and `weapon_types` values. Additionally, each weapon has an array of combat stances associated with it to determine the `combat_style`, `attack_type`, `attack_style` and any `bonuses` or combat `experience` association. The `ItemWeapon` object is nested within an `ItemDefinition` object when using the Python API. If you are parsing the raw JSON files, this data is nested under the `weapon` key.  It is very important to note that not all items in OSRS are equipable weapons. Only items with the `equipable_weapon` property set to `true` are equipable. All of the properties available for equipable weapons are listed in the table below including the property name, the data types used, a description of the property and if the property is required to be populated - if not required, the property value can potentially be set to `None`.

| Property | Data type | Description | Required |
| -------- | --------- | ----------- | -------- |
| attack_speed | integer | The attack speed of a weapon. | Yes |
| weapon_type | string | The weapon classification (e.g., axe) | Yes |
| stances | array | An array of weapon stance information | Yes |

### Item JSON Example

A description of the properties that each item in the database can have is useful, but sometimes it is simpler to provide an example. Below is a full example of an item, specifically the _Abyssal whip_ item. Since this item is a type of equipment, there is an `equipment` key with combat bonuses. Additionally, this item is also a weapon, so there is a `weapon` key with extra information. If the item was not equipable, the `equipment` key would be `null` and the `equipable_by_player` would be `false`. If the item was not a weapon, the `weapon` key would be `null` and the `equipable_weapon` would be `false`.

```
{
    "id": 4151,
    "name": "Abyssal whip",
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

Each monster is represented by Python objects when using the PyPi `osrsbox` package, specifically using Python dataclass objects. - or accessible directly by parsing the raw JSON files. There are two types of objects, or classifications of data, that can be used to represent part of an in-game OSRS monster, each outlined in the following subsections. 

### Monster Definition

An `MonsterDefinition` object type includes basic monster metadata such as `id`, `name`, `examine` text, `combat_level`, `attack_speed` and `hitpoints` values and slayer association such as `slayer_masters` who give this monster as a task. Every monster object in the monster database has all of these properties. If you are parsing the raw JSON files all of these properties are in the root of the JSON document - so they are not nested. All of the properties available are listed in the table below including the property name, the data types used, a description of the property and if the property is required to be populated - if not required, the property value can potentially be set to `None`.

| Property | Data type | Description | Required |
| -------- | --------- | ----------- | -------- |
| id | integer | The ID number of the monster. | Yes |
| name | string | The name of the monster. | Yes |
| incomplete | boolean | If the monster has incomplete wiki data. | Yes |
| members | boolean | If the monster is members only, or not. | Yes |
| release_date | string | The release date of the monster (in ISO8601 format). | No |
| combat_level | integer | The combat level of the monster. | Yes |
| size | integer | The size, in tiles, of the monster. | Yes |
| hitpoints | integer | The number of hitpoints a monster has. | Yes |
| max_hit | integer | The maximum hit of the monster. | Yes |
| attack_type | array | The attack style (melee, magic, range) of the monster. | Yes |
| attack_speed | integer | The attack speed (in game ticks) of the monster. | No |
| aggressive | boolean | If the monster is aggressive, or not. | Yes |
| poisonous | boolean | If the monster poisons, or not | Yes |
| immune_poison | boolean | If the monster is immune to poison, or not | Yes |
| immune_venom | boolean | If the monster is immune to venom, or not | Yes |
| weakness | array | An array of monster weaknesses. | Yes |
| slayer_monster | boolean | If the monster is a potential slayer task. | Yes |
| slayer_level | integer | The slayer level required to kill the monster. | No |
| slayer_xp | integer | The slayer XP rewarded for a monster kill. | No |
| slayer_masters | array | The slayer XP rewarded for a monster kill. | Yes |
| duplicate | boolean | If the monster is a duplicate. | Yes |
| examine | string | The examine text of the monster. | Yes |
| wiki_name | string | The OSRS Wiki name for the monster. | Yes |
| wiki_url | string | The OSRS Wiki URL (possibly including anchor link). | Yes |
| attack_level | integer | The attack level of the monster. | Yes |
| strength_level | integer | The strength level of the monster. | Yes |
| defence_level | integer | The defence level of the monster. | Yes |
| magic_level | integer | The magic level of the monster. | Yes |
| ranged_level | integer | The ranged level of the monster. | Yes |
| attack_stab | integer | The attack stab bonus of the monster. | Yes |
| attack_slash | integer | The attack slash bonus of the monster. | Yes |
| attack_crush | integer | The attack crush bonus of the monster. | Yes |
| attack_magic | integer | The attack magic bonus of the monster. | Yes |
| attack_ranged | integer | The attack ranged bonus of the monster. | Yes |
| defence_stab | integer | The defence stab bonus of the monster. | Yes |
| defence_slash | integer | The defence slash bonus of the monster. | Yes |
| defence_crush | integer | The defence crush bonus of the monster. | Yes |
| defence_magic | integer | The defence magic bonus of the monster. | Yes |
| defence_ranged | integer | The defence ranged bonus of the monster. | Yes |
| attack_accuracy | integer | The attack accuracy bonus of the monster. | Yes |
| melee_strength | integer | The melee strength bonus of the monster. | Yes |
| ranged_strength | integer | The ranged strength bonus of the monster. | Yes |
| magic_damage | integer | The magic damage bonus of the monster. | Yes |
| drops | array | An array of monster drop objects. | Yes |
| rare_drop_table | boolean | If the monster has a chance of rolling on the rare drop table. | Yes |

### Monster Drops

Most monsters in OSRS drop items when they have been defeated (killed). All monster drops are stored in the `drops` property in an array containing properties about the item drop. When using the PyPi `osrsbox` package, these drops are represented by a list of `MonsterDrops` object type. When parsing the raw JSON files, the drops are stored in an array, that are nested under the `drops` key. The data included with the monster drops are the item `id`, item `name`, the drop `rarity`, whether the drop is `noted` and any `drop_requirements`. All of the properties available for item drops are listed in the table below including the property name, the data types used, a description of the property and if the property is required to be populated - if not required, the property value can potentially be set to `None`. 

| Property | Data type | Description | Required |
| -------- | --------- | ----------- | -------- |
| id | integer | The ID number of the item drop. | No |
| name | string | The name of the item drop. | Yes |
| members | boolean | If the drop is a members-only item. | Yes |
| quantity | string | The quantity of the item drop (integer, comma-seperated or range). | No |
| noted | boolean | If the item drop is noted, or not. | Yes |
| rarity | string | The rarity of the item drop (in fraction format). | No |
| drop_requirements | string | If there are any requirements to getting the specific drop. | No |

### Monster JSON Example

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
    "slayer_xp": 150,
    "slayer_masters": [
        "vannaka",
        "chaeldar",
        "konar",
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
            "rarity": "1/1",
            "drop_requirements": null
        },
        {
            "id": 4151,
            "name": "Abyssal whip",
            "members": True,
            "quantity": "1",
            "noted": false,
            "rarity": "1/512",
            "drop_requirements": null
        },
        {
            "id": 13265,
            "name": "Abyssal dagger",
            "members": True,
            "quantity": "1",
            "noted": false,
            "rarity": "1/32768",
            "drop_requirements": null
        },
        {
            "id": 565,
            "name": "Blood rune",
            "members": True,
            "quantity": "7",
            "noted": false,
            "rarity": "4/128",
            "drop_requirements": null
        },
        {
            "id": 19683,
            "name": "Dark totem top",
            "members": True,
            "quantity": "1",
            "noted": false,
            "rarity": "1/350",
            "drop_requirements": "catacombs-only"
        },
        {
            "id": 12073,
            "name": "Clue scroll (elite)",
            "members": True,
            "quantity": "1",
            "noted": false,
            "rarity": "1/1200",
            "drop_requirements": null
        }
    ],
    "rare_drop_table": false
}
```

## The `osrsbox` Python PyPi Package

If you want to access the item and monster database programmatically using Python, the simplest option is to use the [`osrsbox` package available from PyPi](https://pypi.org/project/osrsbox/). You can load the item and/or monster database and process item objects, monster objects, and their properties. 

### Package Quick Start

- Make sure you have >= Python 3.6
- Install package using: `pip install osrsbox`
- Item database quickstart:
    - Import items API using: `from osrsbox import items_api`
    - Load all items using: `all_db_items = items_api.load()`
    - Loop items using: `for item in all_db_items: print(item.name)`
- Monster database quickstart:
    - Import monsters API using: `from osrsbox import monsters_api`
    - Load all monsters using: `all_db_monsters = monsters_api.load()`
    - Loop monsters using: `for monster in all_db_monsters: print(monster.name)`

### Package Requirements

For the `osrsbox` PyPi package you must meet the following requirements:

- Python 3.6 or above
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

## The `osrsbox-db` Static JSON API

This project also includes an Internet-accessible, static JSON API for all items/monsters in the database. The JSON API was originally written for the [`osrsbox-tooltips` project](https://github.com/osrsbox/osrsbox-tooltips) but has since been used for a variety of other projects. The JSON API is useful when you do not want to write a program in Python (as using the PyPi package is probably easier), but would like to fetch the database information programmatically over the Internet, and receive the data back in nicely structured JSON syntax. A key example is a web application. 

### Static JSON API Files

The JSON API is available in the [`docs` folder](https://github.com/osrsbox/osrsbox-db/tree/master/docs/) in the osrsbox-db project repository. This folder contains the publicly available database and somewhat-RESTful API of osrsbox-db (read: not RESTful at all, as it only supports HTTP GET requests). Every file inside this specific folder can be fetched using HTTP GET requests. The base URL for this folder is `https://www.osrsbox.com/osrsbox-db/`. Simply append any name of any file from the `docs` folder to the base URL, and you can fetch this data. You can also clone the entire osrsbox-db project repository and access the files provided in this folder, or download a single file for offline processing. A summary of the folders/files provided in the JSON API are listed below with descriptions:

- `items-complete.json`: A single JSON file that combines all single JSON files from `items-json` folder. This file contains the entire osrsbox-db items database in one file. This is useful if you want to get the data for every single item.
- `items-icons`: Collection of PNG files (20K+) for every item inventory icon in OSRS. Each inventory icon is named using the unique item ID number.
- `items-json`: Collection of JSON files (20K+) of extensive item metadata for every item in OSRS. This folder contains the entire osrsbox-db item database where each item has an individual JSON file, named using the unique item ID number. This is useful when you want to fetch data for a single item where you already know the item ID number.
- `items-json-slot`: Collection of JSON files extracted from the database that are specific for each equipment slot (e.g., head, legs). This is useful when you want to only get item data for equipable items for one, or multiple, specific item slot.
- `items-summary.json`: A single JSON file that contains only the item names and item ID numbers. This file is useful when you want to download a small file (1.1MB) to quickly scan/process item data when you only need the item name and/or ID number.
- `models-summary.json`: A single JSON file that contains model ID numbers for items, objects, and NPCs. This file is useful to determine the model ID number for a specific item, object or NPC.
- `monsters-complete.json`: A single JSON file that combines all single JSON files from the `monsters-json` folder. This file contains the entire osrsbox-db monster database in one file. This is useful if you want to get the data for every single monster in one file.
- `monsters-json`: Collection of JSON files (2.5K+) of extensive monster metadata for every monster in OSRS. This folder contains the entire osrsbox-db monster database where each monster has an individual JSON file, named using the unique monster ID number. This is useful when you want to fetch data for a single monster where you already know the item ID number.
- `npcs-summary.json`: A single JSON file that contains only the NPC names and NPC ID numbers. This file is useful when you want to download a small file (0.35MB) to quickly scan/process NPC data when you only need the NPC name and/or ID number. Note that this file contains both attackable, and non-attackable (monster) NPCs.
- `objects-summary.json`: A single JSON file that contains only the object names and object ID numbers. This file is useful when you want to download a small file (0.86MB) to quickly scan/process in-game object data when you only need the object name and/or ID number.
- `prayer-icon`: Collection of PNG files for each prayer in OSRS.
- `prayer-json`: Collection of individual JSON files with properties and metadata about OSRS prayers.

### Accessing the Static JSON API

The JSON file for each OSRS item can be directly accessed using unique URLs provide through the [`osrsbox.com`](https://www.osrsbox.com/osrsbox-db/) base URL. As mentioned, you can fetch JSON files using a unique URL, but cannot modify any JSON content. Below is a list of URL examples for items and monsters in the osrsbox-db database:

- [`https://www.osrsbox.com/osrsbox-db/items-json/2.json`](https://www.osrsbox.com/osrsbox-db/items-json/2.json)
- [`https://www.osrsbox.com/osrsbox-db/items-json/74.json`](https://www.osrsbox.com/osrsbox-db/items-json/74.json)
- [`https://www.osrsbox.com/osrsbox-db/items-json/35.json`](https://www.osrsbox.com/osrsbox-db/items-json/35.json)
- [`https://www.osrsbox.com/osrsbox-db/items-json/415.json`](https://www.osrsbox.com/osrsbox-db/items-json/415.json)
- [`https://www.osrsbox.com/osrsbox-db/items-json/239.json`](https://www.osrsbox.com/osrsbox-db/items-json/239.json)

As displayed by the links above, each item or monster is stored in the `osrsbox-db` repository, under the [`items-json`](https://github.com/osrsbox/osrsbox-db/tree/master/docs/items-json) folder or [`monsters-json](https://github.com/osrsbox/osrsbox-db/tree/master/docs/monsters-json) folder. In addition to the single JSON files for each item, many other JSON files can be fetched. Some more examples are provided below:

- [`https://www.osrsbox.com/osrsbox-db/items-complete.json`](https://www.osrsbox.com/osrsbox-db/items-complete.json)
- [`https://www.osrsbox.com/osrsbox-db/monsters-complete.json`](https://www.osrsbox.com/osrsbox-db/monsters-complete.json)
- [`https://www.osrsbox.com/osrsbox-db/items-summary.json`](https://www.osrsbox.com/osrsbox-db/items-summary.json)
- [`https://www.osrsbox.com/osrsbox-db/items-json-slot/items-cape.json`](https://www.osrsbox.com/osrsbox-db/items-json-slot/items-cape.json)
- [`https://www.osrsbox.com/osrsbox-db/prayer-json/protect-from-magic.json`](https://www.osrsbox.com/osrsbox-db/prayer-json/protect-from-magic.json)

So how can you get and use these JSON files about OSRS items? It is pretty easy but depends on what you are t- Python 3.6 or above
- Dataclasses package (if Python is below 3.7)rying to accomplish and what programming language you are using. Some examples are provided in the following subsections.

### Accessing the JSON API using Command Line Tools

Take a simple example of downloading a single JSON file. In a Linux system, we could use the `wget` command to download a single JSON file, as illustrated in the example code below:

```
wget https://www.osrsbox.com/osrsbox-db/items-json/12453.json
```

You could perform a similar technique using the `curl` tool:

```
curl https://www.osrsbox.com/osrsbox-db/items-json/12453.json
```

For Windows users, you could use PowerShell:

```
Invoke-WebRequest -Uri "https://www.osrsbox.com/osrsbox-db/items-json/12453.json" -OutFile "12453.json"
```

### Accessing the JSON API using Python

Maybe you are interested in downloading a single (or potentially multiple) JSON files about OSRS items and processing the information in a Python program. The short script below downloads the `12453.json` file using Python's `urllib` library, loads the data as a JSON object and prints the contents to the console. The code is a little messy, primarily due to supporting both Python 2 and 3 - as you can see from the `try` and `except` importing method implemented.

```
import json

try:
    from urllib.request import urlopen
except ImportError:
    from urllib2 import urlopen

url = ("https://www.osrsbox.com/osrsbox-db/items-json/12453.json")
response = urlopen(url)
data = response.read().decode("utf-8")
json_obj = json.loads(data)
print(json_obj)
```

### Accessing the JSON API using JavaScript

Finally, let's have a look at JavaScript (specifically jQuery) example to fetch a JSON file from the osrsbox-db and build an HTML element to display in a web page. The example below is a very simple method to download the JSON file using the jQuery `getJSON` function. Once we get the JSON file, we loop through the JSON entries and print each key and value (e.g., `name` and _Black wizard hat (g)_) on its own line in a `div` element.

```
<!DOCTYPE html>
<html>
  <head>
    <script src="https://ajax.googleapis.com/ajax/libs/jquery/3.1.1/jquery.min.js"></script>
    <script>
      $(document).ready(function(){
          $("button").click(function(){
              $.getJSON("https://www.osrsbox.com/osrsbox-db/items-json/12453.json", function(result){
                  $.each(result, function(i, field){
                      $("div").append(i + " " + field + "<br>");
                  });
              });
          });
      });
    </script>
  </head>
  <body>
    <button>Get JSON data</button>
    <div></div>
  </body>
</html>
```

## The `osrsbox-db` GitHub Repository 

The [official osrsbox-db GitHub repository](https://github.com/osrsbox/osrsbox-db) hosts the source code for the entire osrsbox-db project. The Python PyPi package is located in the `osrsbox` folder of the official development repository, while the other folders in this repository are used to store essential data and Python modules to build the item database. 

### Using the Development Repostory

If using this repository (the development version), you will need to fulfil some specific requirements. This includes having the following tools available on your system:

- Python 3.6 or above
- Pip - the standard package manager for Python
- Virtualenv - a tool to create isloated virtual environments
- A selection of additional Python packages

As a short example, I configured my Ubuntu 18.04 system to run the development repository code using the following steps:

```
sudo apt update
sudo apt install python3-pip
pip3 insatll virtualenv
```

These three commands will install the `pip3` command, allowing the installation of Python package. Then you can use `pip3` to install the `virtualenv` tool, allowing the creation of a virtualized and isolated Python development environment. Then we can install more Python packages that are used in this project. The PyPi `osrsbox` package requires a variety of Python packages in addition to the mandatory `dataclasses` package. These package requirements are documented in the [`requirements.txt`](https://github.com/osrsbox/osrsbox-db/tree/master/requirements.txt) file. It is recommended to use `virtualenv` tool to set up your environment, then install the specified requirements. As an example, the following workflow is provided for Linux-based environments (make sure `virtualenv`, and `python3` are available first):

```
git clone https://github.com/osrsbox/osrsbox-db.git
cd osrsbox-db
virtualenv venv
source venv/bin/activate
pip3 install -r requirements.txt
```

When you have finished with working in the `osrsbox-db` repository, make sure to deactivate the current `virtualenv` environment using:

```
deactivate
```

### Summary of Respository Structure

- `data`: Collection of useful data files used in the osrsbox-db project. The [`README.md`](github.com/osrsbox/osrsbox-db/tree/master/data/README.md) file has additional information on the purpose of each file in this folder.
- `docs`: The publicly accessible item database available through this repo or by using the static JSON API. This folder contains the actual item database that is publicly available, or browsable within this repository.
- `extraction_tools_cache`: An up-to-date OSRS cache dump (compressed) with associated tools that are used in other parts in this project.
- `extraction_tools_wiki`: Collection of Python modules to extract data from the new (non-Wikia) OSRS Wiki site. There is also dumped data (category page titles and raw wiki text) for items, quests, and monsters that are somewhat-regularly updated.
- `items_builder`: Collection of Python scripts to build the item database. The `builder.py` script is the primary entry point, and the `item_builder.py` module does the processing of each item.
- `monster-builder`: Collection of Python scripts to build the monster database. The `builder.py` script is the primary entry point, and the `monster_builder.py` module does the processing of each monster.
- `osrsbox`: The Python package:
    - `items_api`: The Python API for interacting with the items database. The API has modules to load all items in the database, iterate through items, and access the different item properties.
    - `items_api_examples`: A collection of simple Python scripts that use the `items_api` to provide an example of what can be achieved and how to use the items database.
    - `monsters_api`: The Python API for interacting with the monster database. The API has modules to load all monsters in the database, iterate through items, and access different monster properties.
    - `monsters_api_examples`: A collection of simple Python scripts that use the `monsters_api` to provide an example of what can be achieved and how to use the monster's database.
- `scripts`: A selection of scripts (using Python and BASH) to help automate common tasks.
- `test`: A collection of unit tests, as well as the JSON schemas.
- `CHANGELOG_items.md`: Document of items added, removed or changed in each weekly game update. This is raw cache data and does not contain every modified property in the database.
- `CHANGELOG_monsters.md`: Document of monsters added, removed, or changed in each weekly game update. This is based on raw cache data and does not contain every modified property in the database.

### Item and Monster Database Schema

Technically, the `osrsbox-db` is not really a database - more specifically it should be called a data set. Anyway... the contents in the item/monster database need to adhere to a specified structure, as well as specified data types for each property. This is achieved (documented and tested) using the [JSON Schema project](https://json-schema.org/). The JSON schema is useful to determine:

- The properties that are available for each item
- Mandatory properties for each item (specified in the `required` property)
- The data types of each property (e.g., boolean, integer, string, null)

The JSON schemas are provided with this project in the `test` folder and includes:

1. [`item_schema.json`](github.com/osrsbox/osrsbox-db/tree/master/test/item_schema.json): This file defines the item schema, the defined properties, the property types, and some additional specifications including regex validation, or property type specification.
1. [`monster_schema.json`](github.com/osrsbox/osrsbox-db/tree/master/test/monster_schema.json): This file defines the monster schema, the defined properties, the property types, and some additional specifications including regex validation, or property type specification.

All JSON schema files are authored using Draft version 7 of the JSON schema, so you should be able to validate any JSON files in this project using any library that supports version 7. This project uses the [`jsonschema` PyPi package](https://pypi.org/project/jsonschema/).

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

Additional data to help build this project is sourced from the [OSRS Wiki](https://oldschool.runescape.wiki/). This primarily includes item metadata. As specified by the [Weird Gloop Copyright](https://meta.weirdgloop.org/w/Meta:Copyrights) page, this content is licensed under CC BY-NC-SA 3.0 - [Attribution-NonCommercial-ShareAlike 3.0 Unported](https://creativecommons.org/licenses/by-nc-sa/3.0/) license.

### Project Attribution

The osrsbox-db project is a labor of love. I put a huge amount of time and effort into the project, and I want people to use it. That is the entire reason for its existence. I am not too fussed about attribution guidelines... but if you want to use the project please adhere to the licenses used. Please feel free to link to this repository or my [OSRSBox website](https://www.osrsbox.com/) if you use it in your project - mainly so others can find it, and hopefully use it too!
