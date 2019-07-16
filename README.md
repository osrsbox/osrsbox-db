# osrsbox-db 

[![Build Status](https://travis-ci.org/osrsbox/osrsbox-db.svg?branch=master)](https://travis-ci.org/osrsbox/osrsbox-db) ![PyPI - Python Version](https://img.shields.io/pypi/pyversions/osrsbox.svg) 

[![PyPI version](https://badge.fury.io/py/osrsbox.svg)](https://badge.fury.io/py/osrsbox) ![PyPI - Downloads](https://img.shields.io/pypi/dm/osrsbox.svg)

## A complete and up-to-date database of Old School Runescape (OSRS) items

This repository hosts a complete and up-to-date database of every item in OSRS. **Complete** means it holds every single item in OSRS. **Up-to-date** means this database is updated after every weekly game update to ensure accurate information. 

The item database has extensive properties for each item: a total of 21 properties for every item, and an additional 17 properties for equipable items. Each item has properties including whether an item is tradeable, stackable, or equipable or if the item is members only or an item associated with a quest. For any equipable item, there are additional properties about combat stats the item has; for example, what slash attack bonus, magic defence bonus or prayer bonus an item provides.

The item database is accessible using two primary methods:

1. **A Python PyPi package named `osrsbox`**
1. **A JSON API**

Current development is working towards adding a similar database for monsters.

## Table of Contents

- [Additional Documentation](#additional-documentation)
- [Project Requirements](#project-requirements)
- [The `osrsbox` Package](#the-osrsbox-package)
- [The `osrsbox-db` JSON API](#the-osrsbox-db-JSON-API)
- [Item Database Schema](#item-database-schema)
- [Project Information](#project-information)
    - [Project Structure](#summary-of-project-structure)
    - [Project Feedback](#project-feedback)
    - [Project Contribution](#project-contribution)
    - [Project License](#project-license)
    - [Project Attribution](#project-attribution)

## Additional Documentation

For detailed information about the project see the [OSRSBox](https://www.osrsbox.com/) website for the official project page, and the _Database_ tag to find blog posts about the project: 

- https://www.osrsbox.com/projects/osrsbox-db/
- https://www.osrsbox.com/blog/tags/Database/

## Project Requirements

For the `osrsbox` package (see below) and any scripts in this repository you will need:

- Python 3.6 or above

If using this repository (the development version), you will also need a variety of Python packages. These are split into the general requirements documented in the [`requirements.txt`](requirements.txt) file. It is recommended to use `virtualenv` to setup your environment, then install the specified requirements using:

```
pip install -r requirements.txt
```

## The `osrsbox` Package

If you just want to access the item database programmatically, it is probably more sensible to use the [`osrsbox` package available from PyPi](https://pypi.org/project/osrsbox/). Basically, you can load the item database and process item objects and their properties. 

This repo hosts the source code for the package in the `osrsbox` folder, while the other folders in this repository are used to store essential data and Python modules to build the item database. You can install the `osrsbox` package using `pip`:

```
pip install osrsbox
```

More information regarding using the `osrsbox` Python package can be found in the [`osrsbox` package README file](osrsbox/README.md).

## The `osrsbox-db` JSON API

This project also includes an Internet-accessible JSON API for all items in the item database. The JSON API was originally written for the [`osrsbox-tooltips` project](https://github.com/osrsbox/osrsbox-tooltips) but has been used for a variety of other projects. The JSON API is useful when you do not want to write a program in Python, but would like to fetch the item database information programmatically. A key example is a web application. 

The JSON API is available in the [`docs` folder](docs/) in this repository. More information regarding using the `osrsbox-db` JSON API can be found in the [`osrsbox-db` README file](docs/README.md).

## Item Database Schema

Technically, the `osrsbox-db` is not really a database - more specifically it should be called a data set. Anyway... the contents in the item database need to adhere to a specified structure, as well as specified data types for each property. This is achieved (documented and tested) using the [JSON Schema project](https://json-schema.org/). The JSON schema is provided with this project in the [`item_schema.json` file in the test directory](test/item_schema.json). The JSON schema is useful to determine:

- The properties that are available for each item
- Mandatory properties for each item (specified in the `required` property)
- The data types of each property (e.g., boolean, integer, string, null) 

A more user-friendly table of the currently available item properties can be found in the [`osrsbox` package README file](osrsbox/README.md).

## Project Information

This section contains additional information about the `osrsbox-db` project.

### Summary of Project Structure

- `data`: Collection of useful data files used in the osrsbox-db project.
- `docs`: The publicly accessible item database available through this repo or by using the JSON API. This folder contains the actual item database that is publicly available, or browsable within this repository.
- `extraction_tools_cache`: An up-to-date OSRS cache dump (compressed) with associated tools used in other parts in this project.
- `extraction_tools_wiki`: Collection of Python modules to extract data from the new (non-Wikia) OSRS Wiki site. There is also dumped data (category page titles and raw wiki text) for items, quests, and monsters that are somewhat-regularly updated.
- `items_builder`: Collection of Python scripts to build the item database. The `builder.py` script is the primary entry point.
    - `update_tools`: Scripts used to update all data files after each weekly game update. 
- `osrsbox`: The Python package:
    - `items_api`: The Python API for interacting with the items database. Has modules to load all items in the database, iterate through items and access the different item properties.
    - `items_tools`: A collection of simple Python scripts that use the `items_api` to provide an example of what can be achieved and how to use the items database.
- `scripts`: A selection of scripts (using Python) to help automate common tasks.
- `test`: A collection of unit tests.
- `CHANGELOG_items.md`: Document of items added, removed or changed in each weekly game update that has been added to the database.
 
 ### Project Feedback

I would thoroughly appreciate any feedback regarding the osrsbox-db project, especially problems with the inaccuracies of the data provided. So if you notice any problem with the accuracy of item property data, could you please let me know. The same goes for any discovered bugs, or if you have a specific feature request. The best method is to [open a new Github issue](https://github.com/osrsbox/osrsbox-db/issues) in the project repository. 

### Project Contribution

This project would thoroughly benefit from a contribution from additional developers. Please feel free to submit a pull request if you have code that you wish to contribute - I would thoroughly appreciate the helping hand. For any code contributions, the best method is to [open a new GitHub pull request](https://github.com/osrsbox/osrsbox-db/pulls) in the project repository. Also, feel free to contact me (e.g., email) if you wish to discuss contribution before making a pull request.

### Project License

The osrsbox-db project is released under the GNU General Public License version 3 as published by the Free Software Foundation. You can read the [LICENSE](LICENSE) file for the full license, check the [GNU GPL](https://www.gnu.org/licenses/gpl-3.0.en.html) page for additional information, or check the [tl;drLegal](https://tldrlegal.com/license/gnu-general-public-license-v3-(gpl-3) documentation for the license explained in simple English. The GPL license is specified for all source code contained in this project. Other content is specified under GPL if not listed in the **Exceptions to GPL** below.

#### Exceptions to GPL

Old School RuneScape (OSRS) content and materials are trademarks and copyrights of JaGeX or its licensors. All rights reserved. OSRSBox and the osrsbox-db project is not associated or affiliated with JaGeX or its licensors. 

Additional data to help build this project is sourced from the [OSRS Wiki](https://oldschool.runescape.wiki/). This primarily includes item metadata. As specified by the [Weird Gloop Copyright](https://meta.weirdgloop.org/w/Meta:Copyrights) page, this content is licensed under CC BY-NC-SA 3.0 - [Attribution-NonCommercial-ShareAlike 3.0 Unported](https://creativecommons.org/licenses/by-nc-sa/3.0/) license.

### Project Attribution

The osrsbox-db project is a labor of love. I put a huge amount of time and effort into the project, and I want people to use it. That is the entire reason for its existence. I am not too fussed about attribution guidelines... but if you want to use the project please adhere to the licenses used. Please feel free to link to this repository or my [OSRSBox website](https://www.osrsbox.com/) if you use it in your project - mainly so others can find it, and hopefully use it too!
