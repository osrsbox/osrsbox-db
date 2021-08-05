"""
Author:  PH01L
Email:   phoil@osrsbox.com
Website: https://www.osrsbox.com

Description:
Build an item given OSRS cache, wiki and custom data.

Copyright (c) 2021, PH01L

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
from typing import Dict
from pathlib import Path
from datetime import datetime
from datetime import timezone

import mwparserfromhell
from deepdiff import DeepDiff

import config
import validator
from builders.items import infobox_cleaner
from scripts.wiki.wikitext_parser import WikitextTemplateParser
from osrsbox.items_api.item_properties import ItemProperties


class BuildItem:
    def __init__(self, **kwargs):
        # ID number to process
        self.item_id = kwargs["item_id"]
        # Raw cache data for all items
        self.all_items_cache_data = kwargs["all_items_cache_data"]
        # All current item database contents
        self.all_db_items = kwargs["all_db_items"]
        # Raw data dump from OSRS Wiki
        self.all_wikitext_raw = kwargs["all_wikitext_raw"]
        # Processed wikitext for all items
        self.all_wikitext_processed = kwargs["all_wikitext_processed"]
        # Dictionary of unalchable items (using item name)
        self.unalchable = kwargs["unalchable"]
        # Dictionary of item buy limits
        self.buy_limits = kwargs["buy_limits"]
        # Dictionary of item requirements
        self.skill_requirements = kwargs["skill_requirements"]
        # Weapon stances dictionary
        self.weapon_stances = kwargs["weapon_stances"]
        # Dictionary of item icons
        self.icons = kwargs["icons"]
        # A dictionary of know duplicate items
        self.duplicates = kwargs["duplicates"]
        # The item schema
        self.schema_data = kwargs["schema_data"]
        # A list of already known (processed) items
        self.known_items = kwargs["known_items"]
        # Specify verbosity
        self.verbose = kwargs["verbose"]

        # For this item instance, create dictionary for property storage
        self.item_dict = dict()

        self.infobox_version_number = None
        self.item_wikitext = None
        self.wikitext_found_using = None

    def preprocessing(self) -> Dict:
        """Preprocess an item, and set important object variables.

        This function preprocesses every item dumped from the OSRS cache. Various
        properties are set to help further processing. Items are determined if
        they are a linked item (noted/placeholder), or an actual item. The item
        is checked if it is a valid item (has a wiki page, is an actual item etc.).
        Finally, the wikitext (from the OSRS wiki) is found by looking up ID, linked
        ID, name, and normalized name. The `Infobox Item` or `Infobox Pet` is then
        extracted so that the wiki properties can be later processed and populated.

        :return: A dictionary including success and code.
        """
        # Initialize dictionary to return preprocessing status
        status = {
            "status": False,
            "code": None
        }

        # Set item ID variables
        self.item_id_str = str(self.item_id)

        # Load item dictionary of cache data based on item ID
        # This raw cache data is the baseline information about the specific item
        # and can be considered 100% correct and available for every item
        self.item_cache_data = self.all_items_cache_data[self.item_id_str]

        # Set item name variable (directly from the cache dump)
        self.item_name = self.item_cache_data["name"]

        if self.verbose:
            print(f">>> {self.item_id_str} {self.item_name}")

        # Get the linked ID item value, if available
        self.linked_id_item_int = None
        self.linked_id_item_str = None
        if self.item_cache_data["linked_id_item"] is not None:
            self.linked_id_item_int = int(self.item_cache_data["linked_id_item"])
            self.linked_id_item_str = str(self.item_cache_data["linked_id_item"])

        # Determine the ID number to extract
        # Noted and placeholder items should use the linked_id_item property
        # to fill in additional wiki data...
        item_id_to_process_int = None
        if self.item_cache_data["noted"] is True or self.item_cache_data["placeholder"] is True:
            item_id_to_process_int = int(self.linked_id_item_int)
        else:
            item_id_to_process_int = int(self.item_id)

        # Find the wiki page
        has_infobox = False

        # Try to find the wiki data using direct ID number search
        if self.all_wikitext_processed.get(self.item_id_str, None):
            self.item_wikitext = self.all_wikitext_processed.get(self.item_id_str, None)
            self.wikitext_found_using = "id"
            status["code"] = "lookup_passed_id"
            status["status"] = True

        # Try to find the wiki data using linked_id_item ID number search
        elif self.all_wikitext_processed.get(self.linked_id_item_str, None):
            self.item_wikitext = self.all_wikitext_processed.get(self.linked_id_item_str, None)
            self.wikitext_found_using = "linked_id"
            status["code"] = "lookup_passed_linked_id"
            status["status"] = True

        # Try to find the wiki data using direct name search
        elif self.all_wikitext_raw.get(self.item_name, None):
            self.item_wikitext = self.all_wikitext_raw.get(self.item_name, None)
            self.wikitext_found_using = "name"
            status["code"] = "lookup_passed_name"
            status["status"] = True

        else:
            status["code"] = "no_item_wikitext"
            return status

        # Parse the infobox item
        infobox_parser = WikitextTemplateParser(self.item_wikitext)

        # Try extract infobox for item, then pet
        has_infobox = infobox_parser.extract_infobox("infobox item")
        if not has_infobox:
            has_infobox = infobox_parser.extract_infobox("infobox pet")
            if not has_infobox:
                self.template = None
                status["code"] = "no_infobox_template"
                return status

        is_versioned = infobox_parser.determine_infobox_versions()
        versioned_ids = infobox_parser.extract_infobox_ids()

        # Set the infobox version number, default to empty string (no version number)
        try:
            if versioned_ids:
                self.infobox_version_number = versioned_ids[item_id_to_process_int]
        except KeyError:
            if is_versioned:
                self.infobox_version_number = "1"
            else:
                self.infobox_version_number = ""

        # Set the template
        self.template = infobox_parser.template

        status["status"] = True
        return status

    def populate_non_wiki_item(self):
        """Populate an iem that has no wiki page."""
        self.populate_from_cache_data()

        self.item_dict["tradeable"] = False
        self.item_dict["quest_item"] = False

        self.item_dict["weight"] = None
        self.item_dict["buy_limit"] = None
        self.item_dict["release_date"] = None
        self.item_dict["examine"] = None
        self.item_dict["wiki_name"] = None
        self.item_dict["wiki_url"] = None

        self.item_dict["equipable_by_player"] = False
        self.item_dict["equipable_weapon"] = False
        self.item_dict["incomplete"] = True

        try:
            self.item_dict["icon"] = self.icons[self.item_id_str]
        except KeyError:
            self.item_dict["icon"] = self.icons["blank"]

    def populate_wiki_item(self):
        self.populate_from_cache_data()
        self.populate_from_wiki_data_properties()

        if self.item_dict["equipable"]:
            self.populate_from_wiki_data_equipment()
        else:
            self.item_dict["equipable_by_player"] = False
            self.item_dict["equipable_weapon"] = False

        try:
            self.item_dict["icon"] = self.icons[self.item_id_str]
        except KeyError:
            self.item_dict["icon"] = self.icons["blank"]

    def populate_from_cache_data(self):
        """Populate an item using raw cache data.

        This function takes the raw OSRS cache data for the specific item and loads
        all available properties (that are extracted from the cache).
        """
        # Populate properties from cache data
        self.item_dict["id"] = self.item_cache_data["id"]
        self.item_dict["name"] = self.item_cache_data["name"]
        self.item_dict["members"] = self.item_cache_data["members"]
        self.item_dict["stackable"] = self.item_cache_data["stackable"]
        self.item_dict["stacked"] = self.item_cache_data["stacked"]
        self.item_dict["noted"] = self.item_cache_data["noted"]
        self.item_dict["noteable"] = self.item_cache_data["noteable"]
        self.item_dict["linked_id_item"] = self.item_cache_data["linked_id_item"]
        self.item_dict["linked_id_noted"] = self.item_cache_data["linked_id_noted"]
        self.item_dict["linked_id_placeholder"] = self.item_cache_data["linked_id_placeholder"]
        self.item_dict["placeholder"] = self.item_cache_data["placeholder"]
        self.item_dict["equipable"] = self.item_cache_data["equipable"]
        self.item_dict["cost"] = self.item_cache_data["cost"]

        # Set alch properties
        if self.item_cache_data["placeholder"]:
            self.item_dict["lowalch"] = None
            self.item_dict["highalch"] = None
        else:
            self.item_dict["lowalch"] = self.item_cache_data["lowalch"]
            self.item_dict["highalch"] = self.item_cache_data["highalch"]

        # Set new, tradeable on ge property
        self.item_dict["tradeable_on_ge"] = self.item_cache_data["tradeable_on_ge"]
        # Fix for items that are not actually tradeable on the GE
        if self.item_dict["id"] in [2203, 4595, 7228, 7466, 8624, 8626, 8628]:
            self.item_dict["tradeable_on_ge"] = False

    def populate_from_wiki_data_properties(self):
        """Populate item data from a OSRS Wiki Infobox Item template."""
        # STAGE ONE: Determine then set the wiki_name, wiki_url properties

        # Manually set OSRS Wiki name
        if self.wikitext_found_using not in ["id", "linked_id"]:
            # Item found in wiki by ID, cache name is the best option
            wiki_page_name = self.item_name
        else:
            # Item found using direct cache name lookup on wiki page names,
            # So use wiki page name in the item_wikitext array
            wiki_page_name = self.item_wikitext[0]

        wiki_versioned_name = None
        wiki_name = None

        # Get the versioned, or non-versioned, name from the infobox
        if self.infobox_version_number is not None:
            key = "version" + str(self.infobox_version_number)
            wiki_versioned_name = self.extract_infobox_value(self.template, key)
        else:
            wiki_versioned_name = self.extract_infobox_value(self.template, "version")

        # Set the wiki_name property
        if wiki_versioned_name is not None:
            if wiki_versioned_name.startswith("("):
                wiki_name = wiki_page_name + " " + wiki_versioned_name
            else:
                wiki_name = wiki_page_name + " (" + wiki_versioned_name + ")"
        else:
            wiki_name = wiki_page_name

        self.item_dict["wiki_name"] = wiki_name

        # Set the wiki_url property
        if wiki_versioned_name is not None:
            wiki_url = wiki_page_name + "#" + wiki_versioned_name
        else:
            wiki_url = wiki_page_name

        wiki_url = wiki_url.replace(" ", "_")
        self.item_dict["wiki_url"] = "https://oldschool.runescape.wiki/w/" + wiki_url

        # Check if item is not actually able to be alched
        if wiki_name:
            if wiki_name in self.unalchable:
                self.item_dict["lowalch"] = None
                self.item_dict["highalch"] = None
            elif wiki_versioned_name in self.unalchable:
                self.item_dict["lowalch"] = None
                self.item_dict["highalch"] = None

        # STAGE TWO: Extract and set item properties from the infobox template

        # WEIGHT: Determine the weight of an item
        weight = None
        if self.infobox_version_number is not None:
            key = "weight" + str(self.infobox_version_number)
            weight = self.extract_infobox_value(self.template, key)
        if weight is None:
            weight = self.extract_infobox_value(self.template, "weight")
        if weight is not None:
            self.item_dict["weight"] = infobox_cleaner.weight(weight, self.item_id)
        else:
            self.item_dict["weight"] = None
            self.item_dict["incomplete"] = True

        # QUEST: Determine if item is associated with a quest
        quest = None
        if self.infobox_version_number is not None:
            key = "quest" + str(self.infobox_version_number)
            quest = self.extract_infobox_value(self.template, key)
        if quest is None:
            quest = self.extract_infobox_value(self.template, "quest")
        if quest is not None:
            self.item_dict["quest_item"] = infobox_cleaner.quest(quest)
        else:
            # Being here means the extraction for "quest" failed
            key = "questrequired" + str(self.infobox_version_number)
            quest = self.extract_infobox_value(self.template, key)
            if quest is None:
                quest = self.extract_infobox_value(self.template, "questrequired")
            if quest is not None:
                self.item_dict["quest_item"] = infobox_cleaner.quest(quest)
            else:
                self.item_dict["quest_item"] = False

        # Determine the release date of an item
        release_date = None
        if self.infobox_version_number is not None:
            key = "release" + str(self.infobox_version_number)
            release_date = self.extract_infobox_value(self.template, key)
        if release_date is None:
            release_date = self.extract_infobox_value(self.template, "release")
        if release_date is not None:
            self.item_dict["release_date"] = infobox_cleaner.release_date(release_date)
        else:
            self.item_dict["release_date"] = None
            self.item_dict["incomplete"] = True

        # Determine if an item is tradeable
        tradeable = None
        if self.infobox_version_number is not None:
            key = "tradeable" + str(self.infobox_version_number)
            tradeable = self.extract_infobox_value(self.template, key)
        if tradeable is None:
            tradeable = self.extract_infobox_value(self.template, "tradeable")
        if tradeable is not None:
            self.item_dict["tradeable"] = infobox_cleaner.tradeable(tradeable)
        else:
            self.item_dict["tradeable"] = False
            self.item_dict["incomplete"] = True

        # Determine the examine text of an item
        examine = None
        if self.infobox_version_number is not None:
            key = "examine" + str(self.infobox_version_number)
            examine = self.extract_infobox_value(self.template, key)
        if examine is None:
            examine = self.extract_infobox_value(self.template, "examine")
        if examine is not None:
            self.item_dict["examine"] = infobox_cleaner.examine(examine, self.item_dict["name"])
        else:
            # Being here means the extraction for "examine" failed
            key = "itemexamine" + str(self.infobox_version_number)
            examine = self.extract_infobox_value(self.template, key)
            if examine is None:
                examine = self.extract_infobox_value(self.template, "itemexamine")
            if examine is not None:
                self.item_dict["examine"] = infobox_cleaner.examine(examine, self.item_dict["name"])
            else:
                self.item_dict["examine"] = None
                self.item_dict["incomplete"] = True

        # Set item buy limit, if it is tradeable on the GE
        if not self.item_dict["tradeable_on_ge"]:
            self.item_dict["buy_limit"] = None
        else:
            try:
                buy_limit = self.buy_limits[wiki_name]
            except KeyError:
                try:
                    buy_limit = self.buy_limits[self.item_name]
                except KeyError:
                    buy_limit = None

            self.item_dict["buy_limit"] = buy_limit

        # We finished processing, set incomplete to false if not true
        if not self.item_dict.get("incomplete"):
            self.item_dict["incomplete"] = False

    def populate_from_wiki_data_equipment(self) -> bool:
        """Parse the wiki text template and extract item bonus values from it."""
        # Hardcoded item skips - mostly unobtainable or weird items
        if int(self.item_id) in infobox_cleaner.unequipable:
            self.item_dict["equipable"] = False
            self.item_dict["equipment"] = None
            self.item_dict["equipable_by_player"] = False
            self.item_dict["equipable_weapon"] = False
            return

        # Initialize empty equipment dictionary
        self.item_dict["equipment"] = dict()

        # STAGE ONE: EQUIPMENT

        # Extract the infobox bonuses template
        infobox_bonuses_parser = WikitextTemplateParser(self.item_wikitext)
        has_infobox = infobox_bonuses_parser.extract_infobox("infobox bonuses")
        if not has_infobox:
            has_infobox = infobox_bonuses_parser.extract_infobox("infobox_bonuses")
            if not has_infobox:
                # No infobox bonuses found for the item!
                print("populate_from_wiki_data_equipment: No infobox bonuses")
                exit(1)

        # Set the infobox bonuses template
        bonuses_template = infobox_bonuses_parser.template

        # This item must be equipable by a player, set to True
        self.item_dict["equipable_by_player"] = True

        # Initialize a dictionary that maps database_name -> property_name
        # The database_name is used in this project
        # The property_name is used by the OSRS Wiki
        combat_bonuses = {"attack_stab": "astab",
                          "attack_slash": "aslash",
                          "attack_crush": "acrush",
                          "attack_magic": "amagic",
                          "attack_ranged": "arange",
                          "defence_stab": "dstab",
                          "defence_slash": "dslash",
                          "defence_crush": "dcrush",
                          "defence_magic": "dmagic",
                          "defence_ranged": "drange",
                          "melee_strength": "str",
                          "ranged_strength": "rstr",
                          "magic_damage": "mdmg",
                          "prayer": "prayer"
                          }

        # Loop each of the combat bonuses and populate
        for database_name, property_name in combat_bonuses.items():
            value = None
            if self.infobox_version_number is not None:
                key = property_name + str(self.infobox_version_number)
                value = self.extract_infobox_value(bonuses_template, key)
            if value is None:
                value = self.extract_infobox_value(bonuses_template, property_name)
            if value is not None:
                self.item_dict["equipment"][database_name] = infobox_cleaner.stats(value)
            else:
                self.item_dict["equipment"][database_name] = 0
                self.item_dict["incomplete"] = True

        # Slot
        slot = None
        if self.infobox_version_number is not None:
            key = "slot" + str(self.infobox_version_number)
            slot = self.extract_infobox_value(bonuses_template, key)
        if slot is None:
            slot = self.extract_infobox_value(bonuses_template, "slot")
        if slot is not None:
            self.item_dict["equipment"]["slot"] = infobox_cleaner.caller(slot, "slot")
        else:
            print(">>> populate_from_wiki_data_equipment: No slot")
            exit(1)

        # Skill requirements
        try:
            requirements = self.skill_requirements[self.item_id_str]
            self.item_dict["equipment"]["requirements"] = requirements
        except KeyError:
            self.item_dict["equipment"]["requirements"] = None

        # If item is not weapon or 2h, start set defaults and return
        if (self.item_dict["equipment"]["slot"] not in ["weapon", "2h"]):
            self.item_dict["equipable_weapon"] = False
            return

        # STAGE TWO: WEAPONS

        self.item_dict["weapon"] = dict()

        # Attack speed
        attack_speed = None
        if self.infobox_version_number is not None:
            key = "speed" + str(self.infobox_version_number)
            attack_speed = self.extract_infobox_value(bonuses_template, key)
        if attack_speed is None:
            attack_speed = self.extract_infobox_value(bonuses_template, "speed")
        if attack_speed is not None:
            self.item_dict["weapon"]["attack_speed"] = infobox_cleaner.caller(attack_speed, "speed")
        else:
            # If not present, set to 0
            self.item_dict["weapon"]["attack_speed"] = 0

        # Weapon type
        # Extract the CombatStyles template
        infobox_combat_parser = WikitextTemplateParser(self.item_wikitext)
        has_infobox = infobox_combat_parser.extract_infobox("combatstyles")

        if has_infobox:
            # There is a combatstyles infobox, parse it
            # Set the infobox bonuses template
            combat_template = infobox_combat_parser.template
            weapon_type = infobox_cleaner.caller(combat_template, "weapon_type")
            weapon_type = weapon_type.lower()
            self.item_dict["weapon"]["weapon_type"] = weapon_type
            try:
                self.item_dict["weapon"]["stances"] = self.weapon_stances[weapon_type]
            except KeyError:
                print("populate_from_wiki_data_equipment: Weapon type error 1")
                exit(1)

        else:
            # No combatstyles infobox, try get data from bonuses
            weapon_type = self.extract_infobox_value(bonuses_template, "combatstyle")
            weapon_type = weapon_type.lower()
            weapon_type = weapon_type.replace(" ", "_")
            self.item_dict["weapon"]["weapon_type"] = weapon_type
            try:
                self.item_dict["weapon"]["stances"] = self.weapon_stances[weapon_type]
            except KeyError:
                print("populate_from_wiki_data_equipment: Weapon type error 2")
                exit(1)

        # Finally, set the equipable_weapon property to true
        self.item_dict["equipable_weapon"] = True

    def extract_infobox_value(self, template: mwparserfromhell.nodes.template.Template, key: str) -> str:
        """Helper method to extract a value from a template using a specified key.

        This helper method is a simple solution to repeatedly try to fetch a specific
        entry from a wiki text template (a mwparserfromhell template object).

        :param template: A mediawiki wiki text template.
        :param key: The key to query in the template.
        :return value: The extracted template value based on supplied key.
        """
        value = None
        try:
            value = template.get(key).value
            value = value.strip()
            return value
        except ValueError:
            return value

    def check_duplicate_item(self) -> ItemProperties:
        """Determine if this is a duplicate item.

        :return: An ItemProperties object.
        """
        # Start by setting the duplicate property to False
        self.item_dict["duplicate"] = False

        # Check/set last update
        last_update = self.all_db_items.get(self.item_id, None)
        if last_update:
            self.item_dict["last_updated"] = self.all_db_items[self.item_id]["last_updated"]
        else:
            self.item_dict["last_updated"] = datetime.now(timezone.utc).strftime("%Y-%m-%d")

        # Create an ItemProperties object
        item_properties = ItemProperties(**self.item_dict)

        # Check list of known bad duplicates
        if str(item_properties.id) in self.duplicates:
            duplicate_status = self.duplicates[str(item_properties.id)]["duplicate"]
            self.item_dict["duplicate"] = duplicate_status
            return None

        # Check noted, placeholder and noted properties
        # If any of these properties, it must be a duplicate
        if item_properties.stacked or item_properties.noted or item_properties.placeholder:
            self.item_dict["duplicate"] = True
            return None

        # Set the item properties that we want to compare
        correlation_properties = {
            "name": False,
            "wiki_name": False
        }

        # Loop the list of currently (already processed) items
        for known_item in self.known_items:
            # Skip when cache names are not the same
            if item_properties.name != known_item.name:
                continue

            # Check equality of each correlation property
            for cprop in correlation_properties:
                if getattr(item_properties, cprop) == getattr(known_item, cprop):
                    correlation_properties[cprop] = True

            # Check all values in correlation properties are True
            correlation_result = all(value is True for value in correlation_properties.values())

            # If name and wiki_name match, set duplicate property to True
            if correlation_result:
                item_properties.duplicate = True
                self.item_dict["duplicate"] = True
                return item_properties

            # If wiki_name is None, but cache names match...
            # The item must also be a duplicate
            if not item_properties.wiki_name:
                item_properties.duplicate = True
                self.item_dict["duplicate"] = True
                return item_properties

        # If we made it this far, no duplicates were found
        item_properties.duplicate = False
        self.item_dict["duplicate"] = False
        return item_properties

    def compare_new_vs_old_item(self) -> bool:
        """Print the difference between this item and the database."""
        # Create JSON out object to compare
        item_properties = ItemProperties(**self.item_dict)
        current_json = item_properties.construct_json()

        # Try get existing entry (KeyError means it doesn't exist - aka a new item)
        try:
            existing_json = self.all_db_items[self.item_id]
        except KeyError:
            print(f">>> compare_json_files: NEW ITEM: {item_properties.id}")
            print(current_json)
            self.item_dict["last_updated"] = datetime.now(timezone.utc).strftime("%Y-%m-%d")
            return

        if current_json == existing_json:
            self.item_dict["last_updated"] = self.all_db_items[self.item_id]["last_updated"]
            return

        ddiff = DeepDiff(existing_json, current_json, ignore_order=True, exclude_paths="root['icon']")

        if ddiff:
            print(f">>> compare_json_files: CHANGED ITEM: {item_properties.id}: {item_properties.name}")
            print(ddiff)
        self.item_dict["last_updated"] = datetime.now(timezone.utc).strftime("%Y-%m-%d")

    def export_item_to_json(self):
        """Export item to JSON, if requested."""
        item_properties = ItemProperties(**self.item_dict)
        output_dir = Path(config.DOCS_PATH, "items-json")
        item_properties.export_json(True, output_dir)

    def validate_item(self):
        """Use the schema-items.json file to validate the populated item."""
        # Create JSON out object to validate
        item_properties = ItemProperties(**self.item_dict)
        current_json = item_properties.construct_json()

        # Validate object with schema attached
        v = validator.MyValidator(self.schema_data)
        v.validate(current_json)

        # Print any validation errors
        if v.errors:
            print(v.errors)
            exit(1)

        assert v.validate(current_json)
