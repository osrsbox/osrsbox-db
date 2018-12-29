# osrsbox-db: OSRS Other data extraction tools

## all_buy_limits.py

- A simple script to parse the `ge_limits.json` file from the RuneLite client, compare then against the osrsbox-db. The goal is to convert the item ID to name, and extract the buy limit data with it.
- Run using:
- `python3.6 all_buy_limits.py -i ../docs/items-json/`
- `python.exe all_buy_limits.py -i ..\docs\items-json\`

## all_buy_limits.txt

- This document contains a list of item name to buy limits.
- For example:
- `Cannonball|7000`

## ge_limits.json

- This document is from the RuneLite client and contains a list of buy limits
- [Source](https://github.com/runelite/runelite/blob/master/runelite-client/src/main/resources/net/runelite/client/plugins/grandexchange/ge_limits.json)

## item_skill_requirements.py

- This script helps the manual process of entering in item skill requirements.
- `python3.6 item_skill_requirements.py -i ../docs/items-json/`
- `python.exe item_skill_requirements.py -i ..\docs\items-json\`

## item_skill_requirements.json

- This document contains JSON formatted data that maps all equipable item IDs to an array of skill requirements. An example structure is seen below:
- `"1061": [{"skill": "defence", "level": 1}]`

## normalized_names.txt

- This document stores information about OSRS items that are not directly extractable from the OSRS Wiki. The purpose of the document is to aid item metadata extraction by normalizing item names
- The structure of the file is:
    - `itemID|itemName|normalizedName|statusCode`
    - `itemID` is directly from the OSRS client cache
    - `itemName` is directly from the OSRS client cache
    - `nomalizedName` is the itemName normalized for the OSRS Wiki
    - `statusCode` documents specific item scenarios