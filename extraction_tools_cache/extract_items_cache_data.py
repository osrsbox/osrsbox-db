"""
Author:  PH01L
Email:   phoil@osrsbox.com
Website: https://www.osrsbox.com

Description:
Script to generate the items-cache-data.json file by parsing the items.json
compressed cache dump. The items.json file is the compressed, raw ItemDefinitions
that are extracted from the OSRS cache. The resultant file will replace the current
items-scraper.json file that is produced by the itemsscraper RuneLite plugin.

Copyright (c) 2019, PH01L

###############################################################################
This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.
This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.
You should have received a copy of the GNU General Public License
along with this program.  If not, see <http://www.gnu.org/licenses/>.
###############################################################################
"""

import json
from pathlib import Path
from typing import Dict

import config
from extraction_tools_cache.osrs_cache_data import CacheDefinitionFiles


def parse_item_definition(item_data: Dict, definitions: CacheDefinitionFiles, id_number: str) -> Dict:
    """Parse the raw cache ItemDefinition data to a Python dictionary.

    :param item_data: A dictionary holding item properties.
    :param definitions: A dictionary holding the raw ItemDefinition data.
    :param id_number: The item ID number to process
    """
    item_definition = definitions[id_number]
    item_data["name"] = item_definition["name"]
    item_data["tradeable_on_ge"] = item_definition["isTradeable"]
    item_data["members"] = item_definition["members"]

    # Get linked item ID
    if item_definition["notedID"] == -1:
        item_data["linked_id"] = None
    else:
        item_data["linked_id"] = item_definition["notedID"]

    # Get noted ID of item
    if item_definition["notedTemplate"] == 799:
        item_data["noted"] = True
    else:
        item_data["noted"] = False

    # Determine item notability
    if item_definition["notedTemplate"] == 799:
        # Item is noted, so it must be notable
        item_data["noteable"] = True
    elif item_data["linked_id"] is not None:
        if definitions[str(item_data["linked_id"])]["notedTemplate"] == 799:
            # If linked item ID is noted, this item must also be noteable
            item_data["noteable"] = True
    else:
        item_data["noteable"] = False

    # Determine item stackability
    if item_definition["stackable"] == 1:
        item_data["stackable"] = True
    elif item_definition["notedTemplate"] == 799:
        item_data["stackable"] = True
    else:
        item_data["stackable"] = False

    # Determine item equipability
    if "Wear" in item_definition["interfaceOptions"]:
        item_data["equipable"] = True
    elif "Wield" in item_definition["interfaceOptions"]:
        item_data["equipable"] = True
    elif "Equip" in item_definition["interfaceOptions"]:
        item_data["equipable"] = True
    else:
        item_data["equipable"] = False

    # Get cost of item, then determine lowalch and highalch
    item_data["cost"] = item_definition["cost"]
    item_data["lowalch"] = int(item_data["cost"] * 0.4)
    item_data["highalch"] = int(item_data["cost"] * 0.6)

    # Determine if the item is a placeholder
    if item_definition["placeholderTemplateId"] == 14401:
        item_data["placeholder"] = True
    else:
        item_data["placeholder"] = False

    return item_data


def parse_item_definition_fix_noted_item(item_data: Dict, definitions: CacheDefinitionFiles, id_number: str) -> Dict:
    """Parse the raw cache ItemDefinition data to a Python dictionary.

    This function tries to fix any item that is linked, by looking up properties
    from the linked item ID and re-populating the name, members, cost, lowalch
    and highalch properties.

    :param item_data: A dictionary holding item properties.
    :param definitions: A dictionary holding the raw ItemDefinition data.
    :param id_number: The item ID number to process
    """
    item_definition = definitions[id_number]
    item_data["name"] = item_definition["name"]
    item_data["members"] = item_definition["members"]
    item_data["cost"] = item_definition["cost"]
    item_data["lowalch"] = int(item_data["cost"] * 0.4)
    item_data["highalch"] = int(item_data["cost"] * 0.6)
    return item_data


def main():
    """The main function for generating the `data/items-cache-data.json` file"""
    # Set the file for the items.json file, which should be in the same directory as this script
    compressed_json_file = Path() / config.EXTRACTION_CACHE_PATH / "items.json"
    # Initialize the CacheDefinitionFiles object, passing the items.json file as a parameter
    definitions = CacheDefinitionFiles(compressed_json_file)
    # Decompress the item.json cache file
    definitions.decompress_cache_file()

    # Use the class generator to loop the definition file ID numbers in the object
    for id_number in definitions:
        # print(f">>> Processing: {id_number}")

        # Initialize the dictionary to store item properties
        item_data = dict()

        # Fetch the specific item definition being processed
        item_definition = definitions[id_number]

        # Get the item ID
        item_data["id"] = item_definition["id"]

        # Parse the item
        item_data = parse_item_definition(item_data, definitions, id_number)

        if (item_definition["name"] == "null" and
                item_definition["notedTemplate"] == 799):
            # This item is noted (notedTemplate is 799)
            # The linked ID must be queried for name, members, cost, lowalch, highalch
            linked_id_number = str(item_definition["notedID"])
            item_data = parse_item_definition_fix_noted_item(item_data, definitions, linked_id_number)

        elif (item_definition["name"] == "null" and
                item_definition["placeholderTemplateId"] == 14401):
            # This item is a placeholder (placeholderTemplateId is 14401)
            linked_id_number = str(item_definition["placeholderId"])
            # This item needs a name set
            item_data["name"] = definitions[linked_id_number]["name"]

        elif (item_definition["name"] == "null" and
                item_definition["boughtTemplateId"] == 13189):
            # This item is bought (boughtTemplateId is 13189)
            linked_id_number = str(item_definition["boughtId"])
            # This item needs a name set
            item_data["name"] = definitions[linked_id_number]["name"]

        ALL_ITEMS_NEW[str(item_data["id"])] = item_data


if __name__ == "__main__":
    ALL_ITEMS_NEW = dict()

    # Run the main function, then compare the two files
    main()

    # Finally, dump the extracted data to the data dir
    out_fi = Path(config.DATA_PATH / "items-cache-data.json")
    with open(out_fi, "w") as f:
        json.dump(ALL_ITEMS_NEW, f)

    # # Some commented code to compare the items-scraper and items-cache-date files
    # ALL_ITEMS_OLD = dict()
    # scraper_path = Path(config.DATA_PATH / "items-scraper.json")
    # with open(scraper_path) as f:
    #     ALL_ITEMS_OLD = json.load(f)
    # from deepdiff import DeepDiff
    # ddiff = DeepDiff(ALL_ITEMS_OLD, ALL_ITEMS_NEW, ignore_order=True)
    # from pprint import pprint
    # pprint(ddiff)
