## osrsbox-db: Useful data

This folder contains a collection of useful data that is used in the osrsbox-db project.
 
A summary of the contents are listed below with descriptions:

- `attackable-npcs.json`: A JSON file containing NPC definitions from the OSRS cache for NPCs that are attackable.
- `ge-limits-ids.json`: A JSON file that contains all Grand Exchange buy limits from the [`ge_limits.json` file from the RuneLite client](https://github.com/runelite/runelite/blob/master/runelite-client/src/main/resources/net/runelite/client/plugins/grandexchange/ge_limits.json). The file maps the item ID (key) to the buy limit (value).
- `ge-limits-names.json`: A JSON file that contains all Grand Exchange buy limits, generated based on the orgininal `ge_limits.json` file. The file maps the item name (key) to the buy limit (value). 
- `item-skill-requirements.json`: A JSON file that maps the item ID (key) to a dictionary of skill requirements (value) to use the item. This file was generated specifically for the osrsbox-db project.
- `items-scraper.json`: A single JSON file that contains raw item metadata from the OSRS cache. The file is similar to the item definition file extracted by OSRS cache tools, but only contains useful item metadata, and excludes properties such as models and animations.
