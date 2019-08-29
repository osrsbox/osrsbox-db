## osrsbox-db: Useful Data

This folder contains a collection of useful data that is used in the osrsbox-db project. A summary of the data files, their contents and uses are provided in the sections below.

### Monsters Cache Data (Attackable NPCs)

The `monsters-cache-data.json` file is a JSON file containing NPC definitions from the OSRS cache for NPCs that are attackable. The data is extracted from the OSRS Cache using the [`extract_monsters_cache_data.py` script](../extraction_tools_cache/extract_monsters_cache_data.py) which looks for the keyword _Attack_ in `options` array for each NPC definition. The use of the data in the osrsbox-db is when building the Monsters database contents.

### DMM-Only Items

The `dmm-only-items.json` file is a JSON file containing OSRS items (ID and name) that are only available in the Dead Man Mode game. The data is extracted manually using the [Ancient Warriors' equipment page](https://oldschoolrunescape.fandom.com/wiki/Ancient_Warriors%27_equipment) in conjunction with the [`populate_dmm_only_items.py` script](../scripts/helpers/populate_dmm_only_items.py). The use of the data in the osrsbox-db to help developers identify DMM-Only items.

### Grand Exchange Limits

The `ge-limits-ids.json` and `ge-limits-names.json` files are both JSON files that contain buy limit information for items traded on the Grand Exchange. The `ge_limits.json` file is sourced from [the RuneLite client](https://github.com/runelite/runelite/blob/master/runelite-client/src/main/resources/net/runelite/client/plugins/grandexchange/ge_limits.json). The original RuneLite file maps item ID to buy limit. The `ge-limits-ids.json` is the same contents, while the `ge-limits-names.json` file is the same data transformed to map item names to item buy limits. The data is converted using the [`convert_buy_limits.py` script](../scripts/helpers/convert_buy_limits.py). The use of the data in the osrsbox-db is when building the Items database contents.

### Invalid Items

The item definition data in the OSRS Cache is littered with random items that are used in the game... but are not actually items! For example, item icons used in the construction menu system. This file is a list of items that are known to not be items, and has metadata about their actual use in-game. The purpose of the data is to be used as input to help build the item database.

### Item Ammo Requirements  
 
The `item-ammo-requirements.json` file was generated for the osrsbox-db project by the [OSRS Best in Slot website developer](https://www.osrsbestinslot.com/). The JSON file maps item ID number to an object of ammo requirements for the item. The data was manually compiled, but can be automated for checking using the [`item_ammo_requirements.py` script](../scripts/helpers/item_ammo_requirements.py). The script parses the item database contents and looks for equipable items in the `ammo` item slot, then prints to default structure to manually enter the data. 

### Item Skill Requirements  
 
The `item-skill-requirements.json` file was generated specifically for the osrsbox-db project. The JSON file maps item ID number to an object of skill requirements for the item. The data was manually compiled using the [`item_skill_requirements.py` script](../scripts/helpers/item_skill_requirements.py) which parses the item database contents and looks for items without a `requirements` entry, then prints to default structure to manually enter the data. The use of the data in the osrsbox-db is when building the Item database contents.

### Items Cache Data

The `items-cache-data.json` file is extracted and parsed item definition data from the OSRS cache. This used to be generated using a custom RuneLite plugin, but now a Python script named [extract_items_cache_data.py](../extraction_tools_cache/extract_items_cache_data.py) extracts item metadata. 

### Weapon Type/Stance Data

All weapons in OSRS have specific types which associates the weapon with specific combat stance data. The `weapon-stances.json` file has the type of weapon (key) which maps to an array of stance data (value). The `weapon-types.json` file has the item ID (key) mapping to the `weapon_type` that can be mapped to the data in the `weapon-stances.json` file. The data was generated using the [`extract_weapon_data.py` script](../extraction_tools_wiki/extract_weapon_data.py) which parses the _Weapon/Types_ page on the OSRS Wiki.
