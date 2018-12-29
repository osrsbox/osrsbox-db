# osrsbox-db: Item Database API Tools

This folder hosts the code used to interact with the item database. This code is tested and works pretty well for a short and simple implementation. The only requirement to use the API is Python 3. It has not been tested using Python 2.7.

## API Classes

The Python API is comprised as a collection of Python classes. This code provides the ability to load and manage the database of items. When an item is loaded, various checks are performed to make sure all the properties have correct data types. In addition, there is a class to handle every object in the database, to make processing simpler. The four Python classes are described below.

1. `AllItems.py`: Handles (loads and stores) all items in the database
1. `ItemDefinition.py`: Handles an instance of a single item from the database
1. `ItemBonuses.py`: Handles an instance of the item bonuses of a single item from the database (this is for equipable items only)
1. `ItemEquipment.py`: Handles an instance of the item equipment properties of a single item from the database (this is for equipable items only)

## API Tools

Any tool in this folder that is identifiable as it starts with a lowercase letter `c_`. This stands for _caller_ and should help identify the actual tools available and tell them apart from the API classes. The following tools are currently available:

- `c_PrintItemNames.py`: Print the names of every item in the database
- `c_DetermineNewItems.py`: Part of the database update workflow. Put new `items_itemscraper.json` in the same dir, and compare to current database contents to determine new, removed and changed items
- `c_GenerateItemsCompleteFile.py`: Part of the database update workflow. Creates a single `items_complete.json` file after `items-json` is updated
- `c_GenerateItemSlotFiles.py`: Part of the database update workflow. Creates JSON files for different equipment slots
