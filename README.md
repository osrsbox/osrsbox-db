# osrsbox-db 

![build](https://img.shields.io/github/workflow/status/osrsbox/osrsbox-db/Build%20and%20Deploy%20to%20PyPI) ![PyPI - Python Version](https://img.shields.io/pypi/pyversions/osrsbox.svg) 

[![PyPI version](https://badge.fury.io/py/osrsbox.svg)](https://badge.fury.io/py/osrsbox) ![PyPI - Downloads](https://img.shields.io/pypi/dm/osrsbox.svg)

[![Discord Chat](https://img.shields.io/discord/598412106118987787.svg)](https://discord.gg/HFynKyr)

[![Donate](https://img.shields.io/badge/Donate-PayPal-green.svg)](https://www.paypal.com/cgi-bin/webscr?cmd=_s-xclick&hosted_button_id=9J44ADGJQ5BC6&source=url)

## A complete and up-to-date database of Old School Runescape (OSRS) items, monsters and prayers

This project hosts a complete and up-to-date database items, monsters and prayers in OSRS. **Complete** means it holds every single item, monster and prayer in OSRS. **Up-to-date** means this database is updated after every weekly game update to ensure accurate information.

The item database has extensive properties for each item: a total of 27 properties for every item, an additional 16 properties for equipable items, and an additional 3 properties for equipable weapons. These properties include the item ID and name, whether an item is tradeable, stackable, or equipable or if the item is members only. For any equipable item, there are additional properties about combat stats; for example, what slash attack bonus, magic defence bonus or prayer bonus that an item provides. For weapons, additional properties are added which include attack speed, combat stance and weapon type information.

The monster database also has extensive properties: a total of 44 unique properties for each monster, as well as an array of item drops for each monster that has 6 additional properties per item drop. The base properties include the monster ID, name, member status, slayer properties, attack type, max hit, attack types and all monster combat stats. Each monster also has an associated array of drops which document the item ID, name, rarity, quantity, and any requirements to get the drop.

The prayer database documents each prayer that available in-game and has detailed properties: a total of 8 properties for every prayer. The base properties include the prayer name, members status, description, requirements, and bonuses that it provides.

## Table of Contents

- [Project Summary](#project-summary)
- [The `osrsbox` Python PyPi Package](#the-osrsbox-python-pypi-package)
- [The osrsbox RESTful API](#the-osrsbox-restful-api)
- [The osrsbox Static JSON API](#the-osrsbox-static-json-api)
- [The `osrsbox-db` GitHub Repository](#the-osrsbox-db-github-repository)
- [The Item Database](#the-item-database)
- [The Monster Database](#the-monster-database)
- [The Prayer Database](#the-prayer-database)
- [Project Contribution](#project-contribution)
- [Additional Project Information](#additional-project-information)

## Project Summary

The osrsbox-db project provides data for three different categories:

1. **Items**
1. **Monsters**
1. **Prayers**

The osrsbox-db project and data is accessible using four methods:

1. [**The Python PyPi package**](https://pypi.org/project/osrsbox/)
1. [**The RESTful API**](https://github.com/osrsbox/osrsbox-api/)
1. [**The Static JSON API**](https://github.com/osrsbox/osrsbox-db/tree/master/docs)
1. [**The GitHub development repository**](https://github.com/osrsbox/osrsbox-db/)

With four different methods to access data... most people will have the following question: _Which one should I use?_ The following list is a short-sharp summary of the options:

1. [**The Python PyPi package**](https://pypi.org/project/osrsbox/): Use this if you are programming anything in Python - as it is the simplest option. Install using `pip`, and you are ready to do anything from experimenting and prototyping, to building a modern web app using something like Flask.
1. [**The RESTful API**](https://github.com/osrsbox/osrsbox-api/): Use this if you are not programming in Python, and want an Internet-accessible API with rich-quering including filtering, sorting and projection functionality.
1. [**The Static JSON API**](https://github.com/osrsbox/osrsbox-db/tree/master/docs): Use this if you want Internet-accessible raw data (JSON files and PNG images) and don't need queries to filter data. This is a good option if you want to _dump_ the entire database contents, and saves the RESTful API from un-needed traffic.
1. [**The GitHub development repository**](https://github.com/osrsbox/osrsbox-db/): The development repository provides the code and data to build the database. I would not recommend using the development repository unless you are (really) interested in the project or you want to contribute to the project.

## The `osrsbox` Python PyPi Package

If you want to access the item and monster database programmatically using Python, the simplest option is to use the [`osrsbox` package available from PyPi](https://pypi.org/project/osrsbox/). You can load the item and/or monster database and process item objects, monster objects, and their properties. 

### Package Quick Start

- Make sure you have >= Python 3.6
- Install package using: `pip install osrsbox`
- Item database quick start:
    - Import items API using: `from osrsbox import items_api`
    - Load all items using: `items = items_api.load()`
    - Loop items using: `for item in items: print(item.name)`
- Monster database quick start:
    - Import monsters API using: `from osrsbox import monsters_api`
    - Load all monsters using: `monsters = monsters_api.load()`
    - Loop monsters using: `for monster in monsters: print(monster.name)`
- Prayer database quick start:
    - Import prayers API using: `from osrsbox import prayers_api`
    - Load all prayers using: `prayers = prayers_api.load()`
    - Loop prayers using: `for prayer in prayers: print(prayer.name)`

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
>>> items = items_api.load()
>>> for item in items:
...     print(item.id, item.name)
```

Instead of using the Python interpreter, you can also write a simple script and import the `osrsbox` Python package. An example script is provided below, this time for the `monsters_api`:

```
#!/usr/bin/python3

from osrsbox import monsters_api

monsters = monsters_api.load()
for monster in monsters:
    print(monster.id, monster.name)
```

If you would like to review additional examples of using the `osrsbox` Python API, have a look at the [`items_api_examples` folder](https://github.com/osrsbox/osrsbox-db/tree/master/osrsbox/items_api_examples) and [`monsters_api_examples` folder](https://github.com/osrsbox/osrsbox-db/tree/master/osrsbox/monsters_api_examples). There are a number of scripts available that provide examples of loading and processing data using the Python API. 

## The osrsbox RESTful API

The [official osrsbox-api GitHub repository](https://github.com/osrsbox/osrsbox-api) hosts the source code used for the RESTful API. The official `osrsbox-api` project is available from:

- [https://api.osrsbox.com](https://api.osrsbox.com)

The link provided above has an API landing page with detailed information on the project including a project summary, API endpoints, and links to useful documentation. Also, have a look at the [official `osrsbox-api` project README](https://github.com/osrsbox/osrsbox-api/blob/master/README.md) for more information. The README has a tutorial on how to build the API docker environment locally for testing purposes which might be useful.

## The `osrsbox` Static JSON API

This project also includes an Internet-accessible, static JSON API for all items/monsters in the database. The JSON API was originally written for the [`osrsbox-tooltips` project](https://github.com/osrsbox/osrsbox-tooltips) but has since been used for a variety of other projects. The JSON API is useful when you do not want to write a program in Python (as using the PyPi package is probably easier), but would like to fetch the database information programmatically over the Internet, and receive the data back in nicely structured JSON syntax. A key example is a web application. 

### Static JSON API Files

The JSON API is available in the [`docs` folder](https://github.com/osrsbox/osrsbox-db/tree/master/docs/) in the osrsbox-db project repository. This folder contains the publicly available database. Every file inside this specific folder can be fetched using HTTP GET requests. The base URL for this folder is `https://www.osrsbox.com/osrsbox-db/`. Simply append any name of any file from the `docs` folder to the base URL, and you can fetch this data. A summary of the folders/files provided in the JSON API are listed below with descriptions:

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

As displayed by the links above, each item or monster is stored in the `osrsbox-db` repository, under the [`items-json`](https://github.com/osrsbox/osrsbox-db/tree/master/docs/items-json) folder or [`monsters-json`](https://github.com/osrsbox/osrsbox-db/tree/master/docs/monsters-json) folder. In addition to the single JSON files for each item, many other JSON files can be fetched. Some more examples are provided below:

- [`https://www.osrsbox.com/osrsbox-db/items-complete.json`](https://www.osrsbox.com/osrsbox-db/items-complete.json)
- [`https://www.osrsbox.com/osrsbox-db/monsters-complete.json`](https://www.osrsbox.com/osrsbox-db/monsters-complete.json)
- [`https://www.osrsbox.com/osrsbox-db/items-summary.json`](https://www.osrsbox.com/osrsbox-db/items-summary.json)
- [`https://www.osrsbox.com/osrsbox-db/items-json-slot/items-cape.json`](https://www.osrsbox.com/osrsbox-db/items-json-slot/items-cape.json)
- [`https://www.osrsbox.com/osrsbox-db/prayer-json/protect-from-magic.json`](https://www.osrsbox.com/osrsbox-db/prayer-json/protect-from-magic.json)

So how can you get and use these JSON files about OSRS items? It is pretty easy but depends on what you are trying to accomplish and what programming language you are using. Some examples are provided in the following subsections.

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

### Using the Development Repository

If using this repository (the development version), you will need to fulfill some specific requirements. This includes having the following tools available on your system:

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
- `data`: Collection of useful data files used in the osrsbox-db project.
    - `cache`: OSRS client cache dump (not present in repository due to size, but populated using the `scripts/cache` scripts).
    - `icons`: Item and prayer icons in base64.
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
    - `icons`: Various scripts to help process, check or update item icons.
    - `items`: A collection of scripts to help process data for the item builder.
    - `monsters`: A collection of scripts to help process data for the monster builder.
    - `update`: A collection of scripts for automating the data collection and database regeneration.
    - `wiki`: A collection of scripts for automating data extraction from the OSRS Wiki using the MediaWiki API.
- `test`: A collection of PyTest tests.

### Item, Monster and Prayer Database Schemas

Technically, the `osrsbox-db` is not really a database - more specifically it should be called a data set. Anyway... the contents in the item/monster/prayer database need to adhere to a specified structure, as well as specified data types for each property. This is achieved (documented and tested) using the [Cerberus project](https://docs.python-cerberus.org/en/stable/). The Cerberus schema is useful to determine the properties that are available for each entity, and the types and requirements for each property, including:

- `type`: Specifies the data type (e.g., boolean, integer, string)
- `required`: If the property must be populated (true or false)
- `nullable`: If the property can be set to `null` or `None`

The Cerberus schemas are provided in a dedicated repository called [`osrsbox/schemas`](https://github.com/osrsbox/schemas), and implorted into this project as a submodule - this is because the schemas are used in other repositories and central management is required. The schemas are loaded into the `data/schemas` folder and includes:

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
| last_updated | string | The last time (UTC) the item was updated (in ISO8601 date format). | True | False |
| incomplete | boolean | If the item has incomplete wiki data. | True | False |
| members | boolean | If the item is a members-only. | True | False |
| tradeable | boolean | If the item is tradeable (between players and on the GE). | True | False |
| tradeable_on_ge | boolean | If the item is tradeable (only on GE). | True | False |
| stackable | boolean | If the item is stackable (in inventory). | True | False |
| stacked | integer | If the item is stacked, indicated by the stack count. | True | True |
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
| lowalch | integer | The low alchemy value of the item (cost * 0.4). | True | True |
| highalch | integer | The high alchemy value of the item (cost * 0.6). | True | True |
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
| weapon_type | string | The weapon classification (e.g., axes) | True | False |
| stances | list | An array of weapon stance information. | True | False |

### Item: Python Object Example

A description of the properties that each item in the database can have is useful, but sometimes it is simpler to provide an example. Below is a full example of an item as loaded in a Python object, specifically the _Abyssal whip_ item. Since this item is a type of equipment, there is an `EquipmentProperties` object nested with combat bonuses. Additionally, this item is also a weapon, so there is a `WeaponProperties` object with extra information. If the item was not equipable, the `EquipmentProperties` property would be `None` and the `equipable_by_player` would be `False`. If the item was not a weapon, the `WeaponProperties` key would be `None` and the `equipable_weapon` would be `False`.

```
ItemProperties(
    id=4151,
    name='Abyssal whip',
    last_updated='2020-12-27',
    incomplete=False,
    members=True,
    tradeable=True,
    tradeable_on_ge=True,
    stackable=False,
    stacked=None,
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
    icon='iVBORw0KGgoAAAANSUhEUgAAACQAAAAgCAYAAAB6kdqOAAABvUlEQVR4Xu2Xv26DMBDG4QEyZECKIkVCKIoyVR26dOrQpUOHDn3/V3F7nL7689kGAo6z9JNuiH1wP+6PIU3zr2Jq3bRVkQ/Y7feBvfcn93o8upfDwT11XQKwOGQMwfYx9O7rcnaf52GEezuFgNdfn4JQ7RjAQojZLAAMcPJbAOH73PcloBTIQiEAG8MB7Pt6MQ+wSW1QAs6Kh1A/NgtnHyKMcZMUCP3AIBw0XcqmgU9qb4W0JwTIwuRAYHETF4FSIMkORjn1xCnjayy8lN/vLVY7TglfvBRGTJpZrpXM+my1f6DhPRdJs8M3nAPibGDseY9hVgHxzbh3chC22dkPQ8EnufddpBgI69Lk3B8hnPrwOsPEw7FYqUzoOsqBUtps8XUASh0bYbxZxUCcJZzCNnjOBGgDDBRD8d4tQAVgRAqEs2jusLOGEhaCgTQTgApLp/s5A0RBGMg3shx2YZb0fZUz9issD4VpsR4PkJ+uYbczJQr94rW7KT3yDJcegLtqeuRlAFa+0bdoeuTxPV2538Ixt1D86Vutr8IR16CSndzfoSpQLIDh09dmscL5lJICMUClw3JKD8tGXiVgfgACr1tEhnw7UAAAAABJRU5ErkJggg==',
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
        weapon_type='whip',
        stances=[
            {
                'combat_style': 'flick',
                'attack_type': 'slash',
                'attack_style': 'accurate',
                'experience': 'attack',
                'boosts': None
            },
            {
                'combat_style': 'lash',
                'attack_type': 'slash',
                'attack_style': 'controlled',
                'experience': 'shared',
                'boosts': None},
            {
                'combat_style': 'deflect',
                'attack_type': 'slash',
                'attack_style': 'defensive',
                'experience': 'defence',
                'boosts': None
            }
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
    "last_updated": "2020-12-27",
    "incomplete": false,
    "members": true,
    "tradeable": true,
    "tradeable_on_ge": true,
    "stackable": false,
    "stacked": null,
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
    "icon": "iVBORw0KGgoAAAANSUhEUgAAACQAAAAgCAYAAAB6kdqOAAABvUlEQVR4Xu2Xv26DMBDG4QEyZECKIkVCKIoyVR26dOrQpUOHDn3/V3F7nL7689kGAo6z9JNuiH1wP+6PIU3zr2Jq3bRVkQ/Y7feBvfcn93o8upfDwT11XQKwOGQMwfYx9O7rcnaf52GEezuFgNdfn4JQ7RjAQojZLAAMcPJbAOH73PcloBTIQiEAG8MB7Pt6MQ+wSW1QAs6Kh1A/NgtnHyKMcZMUCP3AIBw0XcqmgU9qb4W0JwTIwuRAYHETF4FSIMkORjn1xCnjayy8lN/vLVY7TglfvBRGTJpZrpXM+my1f6DhPRdJs8M3nAPibGDseY9hVgHxzbh3chC22dkPQ8EnufddpBgI69Lk3B8hnPrwOsPEw7FYqUzoOsqBUtps8XUASh0bYbxZxUCcJZzCNnjOBGgDDBRD8d4tQAVgRAqEs2jusLOGEhaCgTQTgApLp/s5A0RBGMg3shx2YZb0fZUz9issD4VpsR4PkJ+uYbczJQr94rW7KT3yDJcegLtqeuRlAFa+0bdoeuTxPV2538Ixt1D86Vutr8IR16CSndzfoSpQLIDh09dmscL5lJICMUClw3JKD8tGXiVgfgACr1tEhnw7UAAAAABJRU5ErkJggg==",
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
        "weapon_type": "whip",
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
| id | integer | Unique OSRS monster ID number. | True | False |
| name | string | The name of the monster. | True | False |
| last_updated | string | The last time (UTC) the monster was updated (in ISO8601 date format). | True | True |
| incomplete | boolean | If the monster has incomplete wiki data. | True | False |
| members | boolean | If the monster is members only, or not. | True | False |
| release_date | string | The release date of the monster (in ISO8601 date format). | True | True |
| combat_level | integer | The combat level of the monster. | True | False |
| size | integer | The size, in tiles, of the monster. | True | False |
| hitpoints | integer | The number of hitpoints a monster has. | True | True |
| max_hit | integer | The maximum hit of the monster. | True | True |
| attack_type | list | The attack style (e.g., melee, magic, range) of the monster. | True | False |
| attack_speed | integer | The attack speed (in game ticks) of the monster. | True | True |
| aggressive | boolean | If the monster is aggressive, or not. | True | False |
| poisonous | boolean | If the monster poisons, or not | True | False |
| venomous | boolean | If the monster poisons using venom, or not | True | False |
| immune_poison | boolean | If the monster is immune to poison, or not | True | False |
| immune_venom | boolean | If the monster is immune to venom, or not | True | False |
| attributes | list | An array of monster attributes. | True | False |
| category | list | An array of monster category. | True | False |
| slayer_monster | boolean | If the monster is a potential slayer task. | True | False |
| slayer_level | integer | The slayer level required to kill the monster. | True | True |
| slayer_xp | float | The slayer XP rewarded for a monster kill. | True | True |
| slayer_masters | list | The slayer masters who can assign the monster. | True | False |
| duplicate | boolean | If the monster is a duplicate. | True | False |
| examine | string | The examine text of the monster. | True | False |
| wiki_name | string | The OSRS Wiki name for the monster. | True | False |
| wiki_url | string | The OSRS Wiki URL (possibly including anchor link). | True | False |
| attack_level | integer | The attack level of the monster. | True | False |
| strength_level | integer | The strength level of the monster. | True | False |
| defence_level | integer | The defence level of the monster. | True | False |
| magic_level | integer | The magic level of the monster. | True | False |
| ranged_level | integer | The ranged level of the monster. | True | False |
| attack_bonus | integer | The attack bonus of the monster. | True | False |
| strength_bonus | integer | The strength bonus of the monster. | True | False |
| attack_magic | integer | The magic attack of the monster. | True | False |
| magic_bonus | integer | The magic bonus of the monster. | True | False |
| attack_ranged | integer | The ranged attack of the monster. | True | False |
| ranged_bonus | integer | The ranged bonus of the monster. | True | False |
| defence_stab | integer | The defence stab bonus of the monster. | True | False |
| defence_slash | integer | The defence slash bonus of the monster. | True | False |
| defence_crush | integer | The defence crush bonus of the monster. | True | False |
| defence_magic | integer | The defence magic bonus of the monster. | True | False |
| defence_ranged | integer | The defence ranged bonus of the monster. | True | False |
| drops | list | An array of monster drop objects. | True | False |

### Monster Drops

Most monsters in OSRS drop items when they have been defeated (killed). All monster drops are stored in the `drops` property in an array containing properties about the item drop. When using the PyPi `osrsbox` package, these drops are represented by a list of `MonsterDrops` object type. When parsing the raw JSON files, the drops are stored in an array, that are nested under the `drops` key. The data included with the monster drops are the item `id`, item `name`, the drop `rarity`, whether the drop is `noted` and any `drop_requirements`. All of the properties available for item drops are listed in the table below including the property name, the data types used, a description of the property, if the property is required to be populated, and if the property is nullable (able to be set to `null` or `None`).

| Property | Data type | Description | Required | Nullable |
| -------- | --------- | ----------- | -------- |----------|
| id | integer | The ID number of the item drop. | True | False |
| name | string | The name of the item drop. | True | False |
| members | boolean | If the drop is a members-only item. | True | False |
| quantity | string | The quantity of the item drop (integer, comma-separated or range). | True | True |
| noted | boolean | If the item drop is noted, or not. | True | False |
| rarity | float | The rarity of the item drop (as a float out of 1.0). | True | False |
| rolls | integer | Number of rolls from the drop. | True | False |

### Monster: Python Object Example 

A description of the properties that each monster in the database can have is useful, but sometimes it is simpler to provide an example. Below is a full example of a monster, specifically the _Abyssal demon_ monster. Please note that the number of item `drops` key data has been reduced to make the data more readable.

```
MonsterProperties(
    id=415,
    name='Abyssal demon',
    last_updated='2020-12-25',
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
    venomous=False,
    immune_poison=False,
    immune_venom=False,
    attributes=['demon'],
    category=['abyssal demon'],
    slayer_monster=True,
    slayer_level=85,
    slayer_xp=150.0,
    slayer_masters=[
        'vannaka',
        'chaeldar',
        'konar',
        'nieve',
        'duradel'
    ],
    duplicate=False,
    examine='A denizen of the Abyss!',
    wiki_name='Abyssal demon (Standard)',
    wiki_url='https://oldschool.runescape.wiki/w/Abyssal_demon#Standard',
    attack_level=97,
    strength_level=67,
    defence_level=135,
    magic_level=1,
    ranged_level=1,
    attack_bonus=0,
    strength_bonus=0,
    attack_magic=0,
    magic_bonus=0,
    attack_ranged=0,
    ranged_bonus=0,
    defence_stab=20,
    defence_slash=20,
    defence_crush=20,
    defence_magic=0,
    defence_ranged=20,
    drops=
    [
        MonsterDrop(
            id=592,
            name='Ashes',
            members=False,
            quantity='1',
            noted=False,
            rarity=1.0,
            rolls=1
        ),
        ...
        MonsterDrop(
            id=4151,
            name='Abyssal whip',
            members=True,
            quantity='1',
            noted=False,
            rarity=0.001953125,
            rolls=1
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
    "last_updated": "2020-12-25",
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
    "venomous": false,
    "immune_poison": false,
    "immune_venom": false,
    "attributes": [
        "demon"
    ],
    "category": [
        "abyssal demon"
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
    "attack_bonus": 0,
    "strength_bonus": 0,
    "attack_magic": 0,
    "magic_bonus": 0,
    "attack_ranged": 0,
    "ranged_bonus": 0,
    "defence_stab": 20,
    "defence_slash": 20,
    "defence_crush": 20,
    "defence_magic": 0,
    "defence_ranged": 20,
    "drops": [
        {
            "id": 1623,
            "name": "Uncut sapphire",
            "members": true,
            "quantity": "1",
            "noted": false,
            "rarity": 0.009765625,
            "rolls": 1
        },
        ...
        {
            "id": 4151,
            "name": "Abyssal whip",
            "members": true,
            "quantity": "1",
            "noted": false,
            "rarity": 0.001953125,
            "rolls": 1
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
| icon | string | The prayer icon. | True | False |

### Prayer: Python Object Example 

A description of the properties that each prayer in the database can have is useful, but sometimes it is simpler to provide an example. Below is a full example of a prayer, specifically the _Rigour_ prayer, as loaded in the `osrsbox` PyPi Python package.

```
PrayerProperties(
    id=28,
    name='Rigour',
    members=True,
    description='Increases your Ranged attack by 20% and damage by 23%, and your defence by 25%.',
    drain_per_minute=40.0,
    wiki_url='https://oldschool.runescape.wiki/w/Rigour',
    requirements={'prayer': 74, 'defence': 70},
    bonuses={'ranged': 20, 'ranged_strength': 25, 'defence': 23}, 
    icon='iVBORw0KGgoAAAANSUhEUgAAABwAAAAYCAYAAADpnJ2CAAABMklEQVR42rWW3Q0CIRCEjwJ8tgBrMPHZFmzAIny0gOvA+izAGjCYcMwNswucSrLJHT/7McvyM02bSojTfwo7Tv8h3h/PqKFfTSTEYqUuwTRQ9R8Erp0XdV79ANBWw7Y/7Mw2W7mhqDSGxTkC0vf5eqqg2I99CKAOVXZ0mY+Lw/SdgFjHk7DD3xE+hLZsINR2+BQMlXG7Gu8Cc2jyt4KketWWw22HWYTUWqcMsYzVcmIBMFQZqBSxmvl1+xj2Z7XdQByQHbKSDET1qNCB1uuHs1ZhY2NgQ2W9fpbCEaAT0jpLeZAKaQvmJI3OUs5QhHoZqoDuWcr7jDe4lURqL3bcIOsTxwJbxmvdcV0FeQPgPmydpZ3KJvcg904bVNi+GwegCPYgG2D1g6nXfvCu4cdRy9rlDXGzl98mKbMMAAAAAElFTkSuQmCC'
)
```

### Prayer: JSON Example

A description of the properties that each prayer in the database can have is useful, but sometimes it is simpler to provide an example. Below is a full example of a prayer, specifically the _Rigour_ prayer, as a JSON object.

```
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
    },
    "icon": "iVBORw0KGgoAAAANSUhEUgAAABwAAAAYCAYAAADpnJ2CAAABMklEQVR42rWW3Q0CIRCEjwJ8tgBrMPHZFmzAIny0gOvA+izAGjCYcMwNswucSrLJHT/7McvyM02bSojTfwo7Tv8h3h/PqKFfTSTEYqUuwTRQ9R8Erp0XdV79ANBWw7Y/7Mw2W7mhqDSGxTkC0vf5eqqg2I99CKAOVXZ0mY+Lw/SdgFjHk7DD3xE+hLZsINR2+BQMlXG7Gu8Cc2jyt4KketWWw22HWYTUWqcMsYzVcmIBMFQZqBSxmvl1+xj2Z7XdQByQHbKSDET1qNCB1uuHs1ZhY2NgQ2W9fpbCEaAT0jpLeZAKaQvmJI3OUs5QhHoZqoDuWcr7jDe4lURqL3bcIOsTxwJbxmvdcV0FeQPgPmydpZ3KJvcg904bVNi+GwegCPYgG2D1g6nXfvCu4cdRy9rlDXGzl98mKbMMAAAAAElFTkSuQmCC"
}
```

## Project Contribution

This project would thoroughly benefit from contributions from additional developers. Please feel free to submit a pull request if you have code that you wish to contribute - I would thoroughly appreciate the helping hand. For any code contributions, the best method is to [open a new GitHub pull request](https://github.com/osrsbox/osrsbox-db/pulls) in the project repository. Also, feel free to contact me (e.g., on the Discord server) if you wish to discuss contribution before making a pull request. If you are not a software developer and want to contribute, even something as small as _Staring_ this repository really makes my day and keeps me motivated!

### Crowd Sourcing Item Skill Requirements

A really manual part of the item database is the `item.equipment.requirements` data. So far, I have manually populated this data... for over 3,500 items! To keep this project alive, I have stopped adding in this data (as it takes a lot of time). Here is a summary of how the item skill requirements work:

- All item requirements are stored in the [`skill-requirements.json`](https://github.com/osrsbox/osrsbox-db/blob/master/data/items/items-skill-requirements.json) file

- They have a structure of:

```
    "item_id": {
        "skill_name": integer
    },
```

- For example, the Abyssal whip item:

```
    "4151": {
        "attack": 70
    },
```

- For the `skill_name`, the [`schema-items.json`](https://github.com/osrsbox/schemas/blob/67b062b8d8499f80f43a95ff3b72cc40a6a833c9/schema-items.json#L293) file has a list of the allowed values - to help get the correct skill name. For example, `runecraft` and not `runecrafting`!

With some community help (by crowd sourcing) we could keep this data point fresh. If you find an error or want to add in a requirement, and want to contribute, here are the best ways to help:

- GitHub PR: Clone the project repo, make changes to `skill-requirements.json`, submit PR
- GitHub Issue: Submit an issue with the fix. It would really help me if you put the request in the correct JSON format as described above!

FYI - there is currently no quest-associated requirements. This would be a great addition to the project, but seems to be a very complex thing to add.

## Additional Project Information

This section contains additional information about the osrsbox-db project. For detailed information about the project see the [`osrsbox.com`](https://www.osrsbox.com/) website for the official project page, and the _Database_ tag to find blog posts about the project: 

- https://www.osrsbox.com/projects/osrsbox-db/
- https://www.osrsbox.com/blog/tags/Database/

### Project Feedback

I would thoroughly appreciate any feedback regarding the osrsbox-db project, especially problems with the inaccuracies of the data provided. So if you notice any problem with the accuracy of item property data, could you please let me know. The same goes for any discovered bugs, or if you have a specific feature request. The best method is to [open a new Github issue](https://github.com/osrsbox/osrsbox-db/issues) in the project repository. 

### Project License

The osrsbox-db project is released under the GNU General Public License version 3 as published by the Free Software Foundation. You can read the [LICENSE](LICENSE) file for the full license, check the [GNU GPL](https://www.gnu.org/licenses/gpl-3.0.en.html) page for additional information, or check the [tl;drLegal](https://tldrlegal.com/license/gnu-general-public-license-v3-(gpl-3)) documentation for the license explained in simple English. The GPL license is specified for all source code contained in this project. Other content is specified under GPL if not listed in the **Exceptions to GPL** below.

#### Exceptions to GPL

Old School RuneScape (OSRS) content and materials are trademarks and copyrights of JaGeX or its licensors. All rights reserved. OSRSBox and the osrsbox-db project is not associated or affiliated with JaGeX or its licensors. 

Additional data to help build this project is sourced from the [OSRS Wiki](https://oldschool.runescape.wiki/). This primarily includes item and monster metadata that is not available in the OSRS cache. As specified by the [Weird Gloop Copyright](https://meta.weirdgloop.org/w/Meta:Copyrights) page, this content is licensed under CC BY-NC-SA 3.0 - [Attribution-NonCommercial-ShareAlike 3.0 Unported](https://creativecommons.org/licenses/by-nc-sa/3.0/) license.

### Project Attribution

The osrsbox-db project is a labor of love. I put a huge amount of time and effort into the project, and I want people to use it. That is the entire reason for its existence. I am not too fussed about attribution guidelines... but if you want to use the project please adhere to the licenses used. Please feel free to link to this repository or my [OSRSBox website](https://www.osrsbox.com/) if you use it in your project - mainly so others can find it, and hopefully use it too!
