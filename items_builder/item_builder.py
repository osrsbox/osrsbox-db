"""
Author:  PH01L
Email:   phoil@osrsbox.com
Website: https://www.osrsbox.com

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

import os
import json
import logging
from pathlib import Path

import jsonschema
import mwparserfromhell
from deepdiff import DeepDiff

import config
from osrsbox.items_api.item_definition import ItemDefinition
from extraction_tools_wiki import infobox_cleaner
from extraction_tools_wiki.wikitext_parser import WikitextTemplateParser

logger = logging.getLogger(__name__)


class BuildItem:
    def __init__(self, item_id, all_item_cache_data, all_wikitext_processed,
                 all_wikitext_raw, all_db_items,
                 buy_limits_data, skill_requirements_data,
                 weapon_types_data, weapon_stances_data, invalid_items_data,
                 export_item):
        self.item_id = item_id
        self.all_item_cache_data = all_item_cache_data  # Raw cache data for all items
        self.all_wikitext_processed = all_wikitext_processed  # Processed wikitext for all items
        self.all_wikitext_raw = all_wikitext_raw  # Raw data dump from OSRS Wiki
        self.all_db_items = all_db_items  # All current item database contents
        self.buy_limits_data = buy_limits_data  # Dictionary of item buy limits
        self.skill_requirements = skill_requirements_data  # Dictionary of item requirements
        self.weapon_types_data = weapon_types_data  # Weapon type dictionary
        self.weapon_stances_data = weapon_stances_data  # Weapon stances dictionary
        self.invalid_items_data = invalid_items_data  # Dictionary of invalid items
        self.export_item = export_item  # If the JSON should be exported/created

        # For this item instance, create dictionary for property storage
        self.item_dict = dict()

        # Set some important properties used for item building
        self.wiki_page_name = None  # The page name the wikitext is from
        self.infobox_version_number = None  # The version used on the wikitext page
        self.status = None  # Used if the item is special (invalid, normalized etc.)

        # All properties that are available for all items
        self.properties = [
            "id",
            "name",
            "members",
            "tradeable",
            "tradeable_on_ge",
            "stackable",
            "noted",
            "noteable",
            "linked_id_item",
            "linked_id_noted",
            "linked_id_placeholder",
            "placeholder",
            "equipable",
            "equipable_by_player",
            "equipable_weapon",
            "cost",
            "lowalch",
            "highalch",
            "weight",
            "buy_limit",
            "quest_item",
            "release_date",
            "examine",
            "wiki_name",
            "wiki_url"]

        # Additional properties for all equipable items (weapons/armour)
        self.equipment_properties = [
            "attack_stab",
            "attack_slash",
            "attack_crush",
            "attack_magic",
            "attack_ranged",
            "defence_stab",
            "defence_slash",
            "defence_crush",
            "defence_magic",
            "defence_ranged",
            "melee_strength",
            "ranged_strength",
            "magic_damage",
            "prayer",
            "slot",
            "requirements"]

        # Additional properties for all equipable weapons
        self.weapon_properties = [
            "attack_speed",
            "weapon_type",
            "stances"]

    def generate_item_object(self):
        """Generate the `ItemDefinition` object from the item_dict dictiornary."""
        self.item_definition = ItemDefinition(**self.item_dict)

    def compare_new_vs_old_item(self):
        """Compare the newly generated item to the existing item in the database."""
        self.compare_json_files(self.item_definition)

    def export_item_to_json(self):
        """Export item to JSON, if requested."""
        if self.export_item:
            output_dir = os.path.join("..", "docs", "items-json")
            self.item_definition.export_json(True, output_dir)
        logging.debug(self.item_dict)

    def preprocessing(self):
        """Preprocess an item, and set important object variables.

        This function preprocesses every item dumped from the OSRS cache. Various
        properties are set to help further processing. Items are determined if
        they are a linked item (noted/placeholder), or an actual item. The item
        is checked if it is a valid item (has a wiki page, is an actual item etc.).
        Finally, the wikitext (from the OSRS wiki) is found by looking up ID, linked
        ID, name, and normalized name. The `Infobox Item` or `Infobox Pet` is then
        extracted so that the wiki properties can be later processed and populated."""
        # Set item ID variables
        self.item_id_int = int(self.item_id)  # Item ID number as an integer
        self.item_id_str = str(self.item_id)  # Item ID number as a string

        # Load item dictionary of cache data based on item ID
        # This raw cache data is the baseline informaiton about the specific item
        # and can be considered 100% correct and available for every item
        self.item_cache_data = self.all_item_cache_data[self.item_id_str]

        # Set item name variable (directly from the cache dump)
        self.item_name = self.item_cache_data["name"]

        # Log and print item
        logging.debug(f"======================= {self.item_id_str} {self.item_name}")
        # print(f"======================= {self.item_id_str} {self.item_name}")
        logging.debug(f"preprocessing: using the following cache data:")
        logging.debug(self.item_cache_data)

        # Get the linked ID item value, if available
        self.linked_id_item_int = None
        self.linked_id_item_str = None
        if self.item_cache_data["linked_id_item"] is not None:
            self.linked_id_item_int = int(self.item_cache_data["linked_id_item"])
            self.linked_id_item_str = str(self.item_cache_data["linked_id_item"])
        logging.debug(f"preprocessing: Linked item ID: {self.linked_id_item_str}")

        # Determine the ID number to extract
        # Noted and placeholder items should use the linked_id_item property
        # to fill in additional wiki data...
        self.item_id_to_process_int = None
        self.item_id_to_process_str = None
        if self.item_cache_data["noted"] is True or self.item_cache_data["placeholder"] is True:
            self.item_id_to_process_int = int(self.linked_id_item_int)
            self.item_id_to_process_str = str(self.linked_id_item_str)
        else:
            self.item_id_to_process_int = int(self.item_id)
            self.item_id_to_process_str = str(self.item_id)
        logging.debug(f"preprocessing: ID to process: {self.item_id_to_process_str}")

        # Try to determine if the item is invalid
        # This can include not being an actual item, has no wiki page etc.
        self.is_invalid_item = False
        try:
            self.is_invalid_item = self.invalid_items_data[self.item_id_to_process_str]
            self.is_invalid_item = True
            self.status = self.invalid_items_data[self.item_id_to_process_str]["status"]
            self.normalized_name = self.invalid_items_data[self.item_id_to_process_str]["normalized_name"]
        except KeyError:
            self.status = None
            self.normalized_name = None
        logging.debug(f"preprocessing: Invalid details: {self.is_invalid_item} {self.status} {self.normalized_name}")

        # Find the wiki page
        # Set all variables to None (for invalid items)
        self.item_wikitext = None
        self.wikitext_found_using = None
        self.has_infobox = False

        # Try to find the wiki data using direct ID number search
        if self.all_wikitext_processed.get(self.item_id_str, None):
            self.item_wikitext = self.all_wikitext_processed.get(self.item_id_str, None)
            self.wikitext_found_using = "id"

        # Try to find the wiki data using linked_id_item ID number search
        elif self.all_wikitext_processed.get(self.linked_id_item_str, None):
            self.item_wikitext = self.all_wikitext_processed.get(self.linked_id_item_str, None)
            self.wikitext_found_using = "linked_id"

        # Try to find the wiki data using direct name search
        elif self.all_wikitext_raw.get(self.item_name, None):
            self.item_wikitext = self.all_wikitext_raw.get(self.item_name, None)
            self.wikitext_found_using = "name"

        # Try to find the wiki data using normalized_name search
        elif self.all_wikitext_raw.get(self.normalized_name, None):
            self.item_wikitext = self.all_wikitext_raw.get(self.normalized_name, None)
            self.wikitext_found_using = "normalized_name"

        logging.debug(f"preprocessing: self.item_wikitext found using: {self.wikitext_found_using}")

        # If there is no wikitext, and the item is valid, raise a critical error
        if not self.item_wikitext and not self.is_invalid_item:
            logging.critical("CRITICAL: Could not find item_wikitext by id, linked_id_item or name...")
            return False

        # Parse the infobox item
        infobox_parser = WikitextTemplateParser(self.item_wikitext)

        # Try extract infobox for item, then pet
        self.has_infobox = infobox_parser.extract_infobox("infobox item")
        if not self.has_infobox:
            self.has_infobox = infobox_parser.extract_infobox("infobox pet")
            if not self.has_infobox:
                self.template = None
                logging.critical("CRITICAL: Could not find template...")
                return False

        self.is_versioned = infobox_parser.determine_infobox_versions()
        logging.debug(f"preprocessing: Is the infobox versioned: {self.is_versioned}")
        self.versioned_ids = infobox_parser.extract_infobox_ids()
        logging.debug(f"preprocessing: Versioned IDs: {self.versioned_ids}")

        # Set the infobox version number, default to empty string (no version number)
        try:
            if self.versioned_ids:
                self.infobox_version_number = self.versioned_ids[self.item_id_to_process_int]
        except KeyError:
            if self.is_versioned:
                self.infobox_version_number = "1"
            else:
                self.infobox_version_number = ""
        logging.debug(f"preprocessing: infobox_version_number: {self.infobox_version_number}")

        # Set the template
        self.template = infobox_parser.template

        return True

    def populate_item(self):
        """Populate an item after preprocessing it.

        This is called for every item in the OSRS cache dump. Start by populating the
        raw metadata from the cache. Then process invalid items, and """
        # Start by populatng the item from the cache data
        self.populate_from_cache_data()

        # Process an invalid item
        if self.is_invalid_item:
            logging.debug("populate_item: Found and processing an invalid item...")

            if self.status == "unequipable":
                # Cache thinks the item is equipable, but it is not
                self.populate_item_properties_from_wiki_data()
                self.item_dict["equipable_by_player"] = False
                self.item_dict["equipable_weapon"] = False
                return True

            if self.status == "no_bonuses_available":
                # Equipable item with wiki page, but does not have an Infobox Bonuses template
                # This is only ever called on ring slot items, as they sometimes have a
                # wiki page without an Infobox Bonuses template
                self.populate_non_wiki_item()
                self.item_dict["equipment"] = dict()
                for equipment_property in self.equipment_properties:
                    self.item_dict["equipment"][equipment_property] = 0
                self.item_dict["equipment"]["slot"] = "ring"
                self.item_dict["equipment"]["requirements"] = None
                self.item_dict["equipable_by_player"] = True
                self.item_dict["equipable_weapon"] = False
                return True

            if self.status == "normalized":
                # Some items have a wiki page, but lookup by ID, linked ID and item name
                # fail. So use the normalized name from the invalid-items.json file
                self.item_wikitext = self.all_wikitext_raw[self.normalized_name]
                self.wikitext_found_using = "normalized_name"
                infobox_parser = WikitextTemplateParser(self.item_wikitext)
                infobox_parser.extract_infobox("infobox item")
                self.template = infobox_parser.template
                self.populate_item_properties_from_wiki_data()
                self.item_dict["equipable_by_player"] = False
                self.item_dict["equipable_weapon"] = False
                return True

            if self.status == "unobtainable":
                # Some items are unobtainable, set defaults
                self.populate_non_wiki_item()
                return True

            if self.status == "skill_guide_icon":
                # Some items are actually an icon in a skill guide, set defaults
                self.populate_non_wiki_item()
                return True

            if self.status == "construction_icon":
                # Some items are actually an icon in the construction interface, set defaults
                self.populate_non_wiki_item()
                return True

            if self.status == "unhandled":
                # Some items have not been classified, set defaults
                self.populate_non_wiki_item()
                return True

            if self.status == "new_item":
                # Some items are new and have incomplete data, set defaults
                self.populate_non_wiki_item()
                return True

        if not self.item_dict["equipable"]:
            # Process a normal, non-equipable item
            logging.debug("populate_item: Populating a normal item using wiki data...")
            self.populate_item_properties_from_wiki_data()
            self.item_dict["equipable_by_player"] = False
            self.item_dict["equipable_weapon"] = False
            return True

        if self.item_dict["equipable"]:
            # Process an equipable item
            logging.debug("populate_item: Populating an equipable item using wiki data...")
            self.populate_item_properties_from_wiki_data()
            self.populate_equipable_properties_from_wiki_data()
            return True

        # Return false by default, this means the item was not found or processed
        logging.error("populate_item: Item was not processed...")
        return False

    def populate_non_wiki_item(self):
        """Populate an iem that has no wiki page."""
        # Set all item properties to None if they have not been populated
        for prop in self.properties:
            try:
                self.item_dict[prop]
            except KeyError:
                self.item_dict[prop] = None

        # Set equipable item/weapon properties to false
        self.item_dict["equipable_by_player"] = False
        self.item_dict["equipable_weapon"] = False

    def populate_from_cache_data(self):
        """Populate an item using raw cache data.

        This function takes the raw OSRS cache data for the specific item and loads
        all availavle properties (that are extracted from the cache)."""
        # Log, then populate cache properties
        logging.debug("populate_from_cache: Loading item cache data data to object...")
        self.item_dict["id"] = self.item_cache_data["id"]
        self.item_dict["name"] = self.item_cache_data["name"]
        self.item_dict["members"] = self.item_cache_data["members"]
        self.item_dict["tradeable_on_ge"] = self.item_cache_data["tradeable_on_ge"]
        self.item_dict["stackable"] = self.item_cache_data["stackable"]
        self.item_dict["noted"] = self.item_cache_data["noted"]
        self.item_dict["noteable"] = self.item_cache_data["noteable"]
        self.item_dict["linked_id_item"] = self.item_cache_data["linked_id_item"]
        self.item_dict["linked_id_noted"] = self.item_cache_data["linked_id_noted"]
        self.item_dict["linked_id_placeholder"] = self.item_cache_data["linked_id_placeholder"]
        self.item_dict["placeholder"] = self.item_cache_data["placeholder"]
        self.item_dict["equipable"] = self.item_cache_data["equipable"]
        self.item_dict["cost"] = self.item_cache_data["cost"]
        self.item_dict["lowalch"] = self.item_cache_data["lowalch"]
        self.item_dict["highalch"] = self.item_cache_data["highalch"]

    def populate_item_properties_from_wiki_data(self):
        """Populate item data from a OSRS Wiki Infobox Item template."""
        if not self.has_infobox:
            # Cannot populate if there is no infobox!
            self.populate_non_wiki_item()
            logging.error("populate_item_properties_from_wiki_data: No infobox for wiki item.")
            return False

        # STAGE ONE: Determine then set the wiki_name and wiki_url

        # Manually set OSRS Wiki name
        if self.wikitext_found_using not in ["id", "linked_id"]:
            # Item found in wiki by ID, cache name is the best option
            wiki_page_name = self.item_name
        elif self.wikitext_found_using == "normalized":
            # Item found in wiki by normalized name, normalize name is used
            wiki_page_name = self.normalized_name
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

        # STAGE TWO: Extract, process and set item properties from the infobox template

        # WEIGHT: Determine the weight of an item ()
        weight = None
        if self.infobox_version_number is not None:
            key = "weight" + str(self.infobox_version_number)
            weight = self.extract_infobox_value(self.template, key)
        if weight is None:
            weight = self.extract_infobox_value(self.template, "weight")
        if weight is not None:
            self.item_dict["weight"] = infobox_cleaner.clean_weight(weight, self.item_id)
        else:
            self.item_dict["weight"] = None

        # QUEST: Determine if item is associated with a quest ()
        quest = None
        if self.infobox_version_number is not None:
            key = "quest" + str(self.infobox_version_number)
            quest = self.extract_infobox_value(self.template, key)
        if quest is None:
            quest = self.extract_infobox_value(self.template, "quest")
        if quest is not None:
            self.item_dict["quest_item"] = infobox_cleaner.clean_quest(quest)
        else:
            # Being here means the extraction for "quest" failed
            key = "questrequired" + str(self.infobox_version_number)
            quest = self.extract_infobox_value(self.template, key)
            if quest is None:
                quest = self.extract_infobox_value(self.template, "questrequired")
            if quest is not None:
                self.item_dict["quest_item"] = infobox_cleaner.clean_quest(quest)
            else:
                self.item_dict["quest_item"] = None

        # Determine the release date of an item ()
        release_date = None
        if self.infobox_version_number is not None:
            key = "release" + str(self.infobox_version_number)
            release_date = self.extract_infobox_value(self.template, key)
        if release_date is None:
            release_date = self.extract_infobox_value(self.template, "release")
        if release_date is not None:
            self.item_dict["release_date"] = infobox_cleaner.clean_release_date(release_date)
        else:
            self.item_dict["release_date"] = None

        # Determine the examine text of an item ()
        tradeable = None
        if self.infobox_version_number is not None:
            key = "tradeable" + str(self.infobox_version_number)
            tradeable = self.extract_infobox_value(self.template, key)
        if tradeable is None:
            tradeable = self.extract_infobox_value(self.template, "tradeable")
        if tradeable is not None:
            self.item_dict["tradeable"] = infobox_cleaner.clean_tradeable(tradeable)
        else:
            self.item_dict["tradeable"] = False

        # Determine the examine text of an item ()
        examine = None
        if self.infobox_version_number is not None:
            key = "examine" + str(self.infobox_version_number)
            examine = self.extract_infobox_value(self.template, key)
        if examine is None:
            examine = self.extract_infobox_value(self.template, "examine")
        if examine is not None:
            self.item_dict["examine"] = infobox_cleaner.clean_examine(examine, self.item_dict["name"])
        else:
            # Being here means the extraction for "examine" failed
            key = "itemexamine" + str(self.infobox_version_number)
            examine = self.extract_infobox_value(self.template, key)
            if examine is None:
                examine = self.extract_infobox_value(self.template, "itemexamine")
            if examine is not None:
                self.item_dict["examine"] = infobox_cleaner.clean_examine(examine, self.item_dict["name"])
            else:
                self.item_dict["examine"] = None

        # Determine if item has a buy limit ()
        if not self.item_dict["tradeable"]:
            self.item_dict["buy_limit"] = None
        else:
            try:
                self.item_dict["buy_limit"] = int(self.buy_limits_data[self.item_dict["name"]])
                if self.item_dict["noted"]:
                    self.item_dict["buy_limit"] = None
            except KeyError:
                self.item_dict["buy_limit"] = None

        return True

    def populate_equipable_properties_from_wiki_data(self) -> bool:
        """Parse the wiki text template and extract item bonus values from it."""
        # Initialize empty equipment dictionary
        self.item_dict["equipment"] = dict()

        # Extract the infobox bonuses template
        infobox_parser = WikitextTemplateParser(self.item_wikitext)
        has_infobox = infobox_parser.extract_infobox("infobox bonuses")
        if not has_infobox:
            has_infobox = infobox_parser.extract_infobox("infobox_bonuses")
            if not has_infobox:
                # No infobox bonuses found for the item!
                print("populate_equipable_properties: Item has no equipment infobox.")
                logging.critical("populate_equipable_properties: Item has no equipment infobox.")
                quit()

        # Set the template
        template = infobox_parser.template

        # STAGE ONE: EQUIPABLE ITEM

        # This item must be equipable by a player, set to True
        self.item_dict["equipable_by_player"] = True

        # Extract equipable item properties
        self.item_dict["equipment"]["attack_stab"] = self.clean_bonuses_value(template, "astab")
        self.item_dict["equipment"]["attack_slash"] = self.clean_bonuses_value(template, "aslash")
        self.item_dict["equipment"]["attack_crush"] = self.clean_bonuses_value(template, "acrush")
        self.item_dict["equipment"]["attack_magic"] = self.clean_bonuses_value(template, "amagic")
        self.item_dict["equipment"]["attack_ranged"] = self.clean_bonuses_value(template, "arange")
        self.item_dict["equipment"]["defence_stab"] = self.clean_bonuses_value(template, "dstab")
        self.item_dict["equipment"]["defence_slash"] = self.clean_bonuses_value(template, "dslash")
        self.item_dict["equipment"]["defence_crush"] = self.clean_bonuses_value(template, "dcrush")
        self.item_dict["equipment"]["defence_magic"] = self.clean_bonuses_value(template, "dmagic")
        self.item_dict["equipment"]["defence_ranged"] = self.clean_bonuses_value(template, "drange")
        self.item_dict["equipment"]["melee_strength"] = self.clean_bonuses_value(template, "str")
        self.item_dict["equipment"]["ranged_strength"] = self.clean_bonuses_value(template, "rstr")
        self.item_dict["equipment"]["magic_damage"] = self.clean_bonuses_value(template, "mdmg")
        self.item_dict["equipment"]["prayer"] = self.clean_bonuses_value(template, "prayer")

        # Determine the slot for the equipable item
        self.item_dict["equipment"]["slot"] = None
        try:
            self.item_dict["equipment"]["slot"] = self.strip_infobox(template.get("slot").value)
            self.item_dict["equipment"]["slot"] = self.item_dict["equipment"]["slot"].lower()
        except ValueError:
            self.item_dict["equipment"]["slot"] = None
            print("populate_equipable_properties: Could not determine item slot...")
            logging.critical("populate_equipable_properties: Could not determine item slot...")
            quit()

        # Determine the skill requirements for the equipable item
        self.item_dict["equipment"]["requirements"] = None
        try:
            requirements = self.skill_requirements[str(self.item_id)]
            self.item_dict["equipment"]["requirements"] = requirements
        except KeyError:
            self.item_dict["equipment"]["requirements"] = None

        # STAGE TWO: WEAPONS

        # If item is weapon, two-handed, or 2h, start processing the weapon data
        if (self.item_dict["equipment"]["slot"] == "weapon" or
                self.item_dict["equipment"]["slot"] == "two-handed" or
                self.item_dict["equipment"]["slot"] == "2h"):

            self.item_dict["weapon"] = dict()

            # Try set the attack speed of the weapon
            try:
                self.item_dict["weapon"]["attack_speed"] = int(self.strip_infobox(template.get("aspeed").value))
            except ValueError:
                self.item_dict["weapon"]["attack_speed"] = None
                logging.critical("WEAPON: Could not determine weapon attack speed")

                # Item IDs with no known attack speed, set to zero
                if int(self.item_id) in [8871]:
                    self.item_dict["weapon"]["attack_speed"] = 0
                # Salamander fix, set to base attack speed of 5
                elif int(self.item_id) in [10145, 10146, 10147, 10147, 10148, 10149]:
                    self.item_dict["weapon"]["attack_speed"] = 5
                else:
                    pass
                    # quit()

            # Try to set the weapon type of the weapon
            try:
                weapon_type = self.weapon_types_data[str(self.item_dict["id"])]["weapon_type"]
                self.item_dict["weapon"]["weapon_type"] = weapon_type
            except KeyError:
                self.item_dict["weapon"]["weapon_type"] = None
                print("populate_equipable_properties: Could not determine weapon type...")
                logging.critical("populate_equipable_properties: Could not determine weapon type...")
                quit()

            # Try to set stances available for the weapon
            try:
                self.item_dict["weapon"]["stances"] = self.weapon_stances_data[self.item_dict["weapon"]["weapon_type"]]
            except KeyError:
                self.item_dict["weapon"]["stances"] = None
                print("populate_equipable_properties: Could not determine weapon stance...")
                logging.critical("populate_equipable_properties: Could not determine weapon stance...")
                quit()

            # Finally, set the equipable_weapon property to true
            self.item_dict["equipable_weapon"] = True

        else:
            # If the item is not a weapon, two-handed or 2h it is not a weapon
            self.item_dict["equipable_weapon"] = False

        return True

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

    def clean_bonuses_value(self, template: mwparserfromhell.nodes.template.Template, prop: str) -> int:
        """Clean a item bonuses value extracted from a wiki template.

        :param template: A mediawiki wiki text template.
        :param prop: The key to query in the template.
        :return value: The extracted template value that has been int cast.
        """
        value = None

        # Try and get the versioned infobox value
        if self.infobox_version_number is not None:
            key = prop + str(self.infobox_version_number)
            value = self.extract_infobox_value(template, key)

        # If unsuccessful, try and get the normal infoxbox value
        if value is None:
            value = self.extract_infobox_value(template, prop)

        if value is not None:
            value = self.strip_infobox(value)
            if isinstance(value, str):
                if value[0] == "-":
                    if value[1:].isdigit():
                        value = int(value)
                elif value[0] == "+":
                    if value[1:].isdigit():
                        value = int(value)
                else:
                    if value.isdigit():
                        value = int(value)
        else:
            value = 0

        return value

    def strip_infobox(self, value: str) -> str:
        """Generic infobox wiki text cleaner.

        :return clean_value: A cleaned wiki text value.
        """
        # Clean an passed InfoBox string
        clean_value = str(value)
        clean_value = clean_value.strip()
        clean_value = clean_value.replace("[", "")
        clean_value = clean_value.replace("]", "")
        return clean_value

    def compare_json_files(self, item_definition: ItemDefinition) -> bool:
        """Print the difference between this item object, and the item that exists in the database."""
        # Create JSON out object to compare
        current_json = item_definition.construct_json()

        # Try get existing entry (KeyError means it doesn't exist - aka a new item)
        try:
            existing_json = self.all_db_items[self.item_id]
        except KeyError:
            print(f">>> compare_json_files: NEW ITEM: {item_definition.id}")
            print(current_json)
            return

        if current_json == existing_json:
            return

        ddiff = DeepDiff(existing_json, current_json, ignore_order=True)
        logging.debug(f">>> compare_json_files: CHANGED ITEM: {item_definition.id}: {item_definition.name}, {item_definition.wiki_name}")
        print(f">>> compare_json_files: CHANGED ITEM: {item_definition.id}: {item_definition.name}")

        # try:
        #     added_properties = ddiff["dictionary_item_added"]
        #     print("   ", added_properties)
        # except KeyError:
        #     pass

        # try:
        #     changed_properties = ddiff["values_changed"]
        #     for k, v in changed_properties.items():
        #         print("   ", k, v["new_value"])
        # except KeyError:
        #     pass

        print(ddiff)
        return

    def validate_item(self):
        """Use the items-schema.json file to validate the populated item."""
        # Create JSON out object to validate
        current_json = self.item_definition.construct_json()

        # Open the JSON Schema for items
        path_to_schema = Path(config.TEST_PATH / "item_schema.json")
        with open(path_to_schema, 'r') as f:
            schema = json.loads(f.read())

        # Check the populate item object against the schema
        jsonschema.validate(instance=current_json, schema=schema)
