"""
Author:  PH01L
Email:   phoil@osrsbox.com
Website: https://www.osrsbox.com

Description:
Generate the items-cache-data.json file from raw Item Definition files.

Copyright (c) 2020, PH01L

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
from scripts.cache import cache_constants


def parse_item_definition(item_data: Dict, definitions: Dict, id_number: str) -> Dict:
    """Parse the raw cache ItemDefinition data to a Python dictionary.

    :param item_data: A dictionary holding item properties.
    :param definitions: A dictionary holding the raw ItemDefinition data.
    :param id_number: The item ID number to process
    """
    item_definition = definitions[id_number]
    item_data["name"] = item_definition["name"]
    item_data["tradeable_on_ge"] = item_definition["isTradeable"]
    item_data["members"] = item_definition["members"]

    # Determine any linked IDs (item, placeholder, noted)
    item_data["linked_id_item"] = None

    if item_definition["notedID"] != -1 and item_definition["notedTemplate"] != 799:
        item_data["linked_id_noted"] = item_definition["notedID"]
    else:
        item_data["linked_id_noted"] = None

    if item_definition["placeholderId"] != -1 and item_definition["placeholderTemplateId"] != 14401:
        item_data["linked_id_placeholder"] = item_definition["placeholderId"]
    else:
        item_data["linked_id_placeholder"] = None

    # Determine if the item is noted
    if item_definition["notedTemplate"] == 799:
        item_data["noted"] = True
    else:
        item_data["noted"] = False

    # Determine if the item is noteable
    if item_definition["notedTemplate"] == 799:
        # Item is noted, so it must be notable
        item_data["noteable"] = True
    elif item_data["linked_id_noted"] is not None:
        if definitions[str(item_data["linked_id_noted"])]["notedTemplate"] == 799:
            # If linked item ID is noted, this item must also be noteable
            item_data["noteable"] = True
    else:
        item_data["noteable"] = False

    # Determine if the item is a placeholder
    if item_definition["placeholderTemplateId"] == 14401:
        item_data["placeholder"] = True
    else:
        item_data["placeholder"] = False

    # Determine item stackability
    if item_definition["stackable"] == 1:
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

    return item_data


def parse_item_definition_fix_linked_item(item_data: Dict, definitions: Dict, id_number: str) -> Dict:
    """Parse the raw cache ItemDefinition data to a Python dictionary.

    This function tries to fix any item that is linked, by looking up properties
    from the linked item ID and re-populating the name, members, cost, lowalch
    and highalch properties.

    :param item_data: A dictionary holding item properties.
    :param definitions: A dictionary holding the raw ItemDefinition data.
    :param id_number: The item ID number to process.
    """
    item_definition = definitions[id_number]
    item_data["name"] = item_definition["name"]
    item_data["members"] = item_definition["members"]
    item_data["cost"] = item_definition["cost"]
    item_data["lowalch"] = int(item_data["cost"] * 0.4)
    item_data["highalch"] = int(item_data["cost"] * 0.6)
    return item_data


def generate_items_cache_data(definitions: Dict, stacked_variants: Dict):
    """Extract item definition data, and process for builder ingestion.

    :param definitions: The raw cache definitions.
    :param stacked_variants: Dictionary of stacked variant item IDs.
    """
    all_items = dict()

    # Loop the loaded data
    for id_number in definitions:
        # Initialize the dictionary to store each item properties
        item_data = dict()

        # Fetch the specific item definition being processed
        item_definition = definitions[id_number]

        # Get the item ID
        item_data["id"] = item_definition["id"]

        # Parse the item
        item_data = parse_item_definition(item_data, definitions, id_number)

        if item_definition["id"] in stacked_variants:
            # This item is a stacked variant (found in countObj)
            linked_id_number = str(stacked_variants[item_definition["id"]]["id"])
            # Parse linked item id to get missing properties
            item_data = parse_item_definition_fix_linked_item(item_data,
                                                              definitions,
                                                              linked_id_number)
            item_data["linked_id_item"] = int(linked_id_number)
            # Set tradeable_og_ge to False, as stacked variants not tradeable on GE
            item_data["tradeable_on_ge"] = False
            # Manually set "stacked" property to True
            item_data["stacked"] = stacked_variants[item_definition["id"]]["count"]

        elif (item_definition["name"] == "null" and
                item_definition["notedTemplate"] == 799):
            # This item is noted (notedTemplate is 799)
            # The linked ID must be queried for name, members, cost, lowalch, highalch
            linked_id_number = str(item_definition["notedID"])
            item_data = parse_item_definition_fix_linked_item(item_data,
                                                              definitions,
                                                              linked_id_number)
            item_data["linked_id_item"] = int(linked_id_number)

        elif (item_definition["name"] == "null" and
                item_definition["placeholderTemplateId"] == 14401):
            # This item is a placeholder (placeholderTemplateId is 14401)
            linked_id_number = str(item_definition["placeholderId"])
            # This item needs a name set
            item_data["name"] = definitions[linked_id_number]["name"]
            item_data["linked_id_item"] = int(linked_id_number)

        elif (item_definition["name"] == "null" and
                item_definition["boughtTemplateId"] == 13189):
            # This item is bought (boughtTemplateId is 13189)
            linked_id_number = str(item_definition["boughtId"])
            # This item needs a name set
            item_data["name"] = definitions[linked_id_number]["name"]
            item_data["linked_id_item"] = int(linked_id_number)

        elif item_definition["name"] == "null":
            # Skip this item, it is not useful
            continue

        # Check extracted item name, if name is null or empty, skip it
        item_name = item_data["name"].lower()
        if item_name == "null" or item_name == "":
            # Skip this item, it is not useful
            continue

        # Check if stacked property is set
        try:
            int(item_data["stacked"])
        except KeyError:
            item_data["stacked"] = None

        all_items[str(item_data["id"])] = item_data

    # Finally, dump the extracted data to the items-cache-data.json file
    out_fi = Path(config.DATA_CACHE_PATH / "items-cache-data.json")
    with open(out_fi, "w") as f:
        json.dump(all_items, f, indent=4)


def find_stacked_variants(definitions: Dict):
    """Extract find all stacked item variants in ItemDefinition data.

    :param definitions: The raw cache definitions.
    """
    stacked_variants = dict()

    # Loop the loaded data
    for id_number in definitions:
        # Fetch the specific item definition being processed
        item_definition = definitions[id_number]

        # Determine if item has stacked variants
        try:
            is_stacked = item_definition["countObj"]
        except KeyError:
            is_stacked = False

        # Process stacked items
        if is_stacked:
            for stacked_id, stacked_count in zip(item_definition["countObj"], item_definition["countCo"]):
                # Skip any entry that is a zero (empty)
                if stacked_id == 0:
                    pass
                else:
                    # Skip any ID that has already been processed
                    if stacked_id in stacked_variants:
                        pass
                    else:
                        stacked_dict = dict()
                        stacked_dict["id"] = item_definition["id"]
                        stacked_dict["count"] = stacked_count
                        stacked_variants[stacked_id] = stacked_dict

    # Sort list of stacked items
    item_ids = [x for x in stacked_variants]
    item_ids.sort(key=int)
    sorted_stacked_variants = dict()
    for item_id in item_ids:
        sorted_stacked_variants[item_id] = stacked_variants[item_id]

    # Finally, dump the extracted stacked item IDs to the items-cache-data.json file
    out_fi = Path(config.DATA_ITEMS_PATH / "stacked-items.json")
    with open(out_fi, "w") as f:
        json.dump(sorted_stacked_variants, f, indent=4)

    return sorted_stacked_variants


if __name__ == "__main__":
    # Determine items with stacked variants. Example:
    # 23663: 23661
    stacked_variants = find_stacked_variants(cache_constants.ITEM_DEFINITIONS)
    # Extract cache data
    generate_items_cache_data(cache_constants.ITEM_DEFINITIONS,
                              stacked_variants)
