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
import logging
import mwparserfromhell

from osrsbox.items_api.item_definition import ItemDefinition
from osrsbox.items_api.item_stats import ItemStats
from osrsbox.items_api.item_equipment import ItemEquipment
from items_builder import infobox_cleaner


class BuildItem:
    def __init__(self, item_id, item_json, wiki_text, normalized_names, buy_limits, skill_requirements, current_db):
        # Input item ID number
        self.item_id = item_id
        # Input JSON file (from RuneLite ItemScraper plugin)
        self.item_json = item_json

        # Input data
        self.wiki_text = wiki_text  # Dict of raw wiki text from OSRS Wiki
        self.normalized_names = normalized_names  # Maps cache names to OSRS Wiki names
        self.buy_limits = buy_limits  # Dictionary of item buy limits
        self.skill_requirements = skill_requirements  # Dictionary of item requirements
        self.current_db = current_db  # Dictionary dump of current database contents

        # For this item, initialize the required objects
        self.itemDefinition = ItemDefinition()
        self.itemDefinition.item_stats = ItemStats()
        self.itemDefinition.item_equipment = ItemEquipment()

        # Setup logging
        logging.basicConfig(filename="builder.log",
                            filemode='a',
                            level=logging.DEBUG)
        self.logger = logging.getLogger(__name__)

        # If a page does not have a wiki page, it may be given a status number
        self.status_code = None

        self.properties = [
            "id",
            "name",
            "members",
            "tradeable",
            "tradeable_on_ge",
            "stackable",
            "noted",
            "noteable",
            "linked_id",
            "equipable",
            "cost",
            "lowalch",
            "highalch",
            "weight",
            "buy_limit",
            "quest_item",
            "release_date",
            "examine",
            "url"]

        self.stat_properties = [
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
            "prayer"]

        self.equipment_properties = [
            "attack_speed",
            "slot",
            "skill_reqs"]

    def populate(self):
        """The primary entry and item object population function."""
        # Start section in logger
        self.logger.debug("============================================ START")
        self.logger.debug(f"item_id: {self.item_id}")

        # STAGE ZERO: CREATE OBJECTS
        self.logger.debug("STAGE ZERO: Create object...")

        # Also, load blank equipable item properties
        if self.itemDefinition.equipable:
            self.equipable_item_set_default()

        # STAGE ONE: LOAD ITEM SCRAPER DATA
        self.logger.debug("STAGE ONE: Loading item-scraper.json data to object...")

        self.populate_from_scraper()

        self.logger.debug(f"id: {self.itemDefinition.id}|name: {self.itemDefinition.name}")
        # print(f"<<<<<<<<<<<<<< id: {self.itemDefinition.id}\tname: {self.itemDefinition.name}")

        # STAGE TWO: DETERMINE WIKI PAGE
        self.logger.debug("STAGE TWO: Determining OSRS Wiki page...")

        has_wiki_page = self.determine_wiki_page()

        # # This commented code can be used to determine wiki page normalization
        # # You must comment out the normalization lookup in determine_wiki_page
        # # WARNING: Does not check equipable item infobox extraction errors!
        # if not has_wiki_page:
        #     if str(self.itemDefinition.id) in self.normalized_names:
        #         normalized_name = self.normalized_names[str(self.itemDefinition.id)][1]
        #         if normalized_name == "" or not normalized_name:
        #             normalized_name = self.itemDefinition.name
        #         status = self.normalized_names[str(self.itemDefinition.id)][2]
        #         print(f"{self.itemDefinition.id}|{self.itemDefinition.name}|{normalized_name}|{status}")
        #     else:
        #         print(f"TODO:{self.itemDefinition.id}|{self.itemDefinition.name}|{self.itemDefinition.name}|X")

        if not has_wiki_page:
            # These will be items that cannot be processed and the program should exit
            print(">>> Cannot find wiki page...")
            print(f"{self.itemDefinition.id}|{self.itemDefinition.name}|{self.itemDefinition.name}|2")
            quit()

        # STAGE THREE: EXTRACT and PARSE INFOBOX
        self.logger.debug("STAGE THREE: Extracting the infobox...")

        # Extract the infobox for the item
        has_infobox = self.extract_infobox()

        # Handle the infobox extraction, depending on the item status code
        if has_infobox:
            self.logger.debug("INFOBOX: Success")
            self.parse_primary_infobox()
        elif self.status_code == 1:
            self.logger.debug("INFOBOX: Invalid item saved")
            return  # Cannot do any other population
        elif self.status_code == 2:
            self.logger.debug("INFOBOX: Unobtainable item saved")
            return  # Cannot do any other population
        elif self.status_code == 3:
            self.logger.debug("INFOBOX: Unusable item saved")
            return  # Cannot do any other population
        elif self.status_code == 4:
            self.logger.debug("INFOBOX: Not really an item, item saved")
            return  # Cannot do any other population
        elif self.status_code == 5:
            self.logger.debug("INFOBOX: No dedicated wiki page for item, saved")
            return  # Cannot do any other population
        elif self.status_code == 6:
            self.logger.debug("INFOBOX: No item bonuses")
            self.parse_primary_infobox()
            return  # Cannot do any other population
        else:
            self.logger.critical("INFOBOX: Extraction error.")
            quit()

        # STAGE FOUR: PARSE INFOBOX FOR EQUIPABLE ITEMS
        self.logger.debug("STAGE FIVE: Parsing the bonuses...")

        if self.itemDefinition.equipable and has_wiki_page:
            # Continue processing... but only if the item is equipable
            has_infobox_bonuses = self.extract_bonuses()
            if has_infobox_bonuses:
                self.logger.debug("Item InfoBox Bonuses extracted successfully")
            else:
                self.logger.critical("Item InfoBox Bonuses extraction error.")
                self.logger.critical("Status Code: %s" % self.status_code)
                print(">>> ERROR: Could not determine equipable item bonuses...")
                quit()

        # STAGE FIVE: COMPARE TO CURRENT DATABASE CONTENTS
        self.logger.debug("STAGE FIVE: Compare object to existing database entry...")

        self.compare_json_files()
        json_out = self.itemDefinition.construct_json()
        self.logger.debug(json_out)

        self.logger.debug("============================================ END")

        # Actually output a JSON file, comment out for testing
        output_dir = os.path.join("..", "docs", "items-json")
        self.itemDefinition.export_json(True, output_dir)

    def populate_from_scraper(self):
        """Populate the itemDefinition object from the item-scraper file content."""
        self.itemDefinition.id = self.item_json["id"]
        if self.item_json["name"] in [None, "null", "Null", ""]:
            self.itemDefinition.name = None
        else:
            self.itemDefinition.name = self.item_json["name"]
        # Need to set these properties
        self.itemDefinition.members = self.item_json["members"]
        self.itemDefinition.tradeable_on_ge = self.item_json["tradeable_on_ge"]
        self.itemDefinition.stackable = self.item_json["stackable"]
        self.itemDefinition.noted = self.item_json["noted"]
        self.itemDefinition.noteable = self.item_json["noteable"]
        self.itemDefinition.linked_id = self.item_json["linked_id"]
        self.itemDefinition.equipable = self.item_json["equipable"]
        self.itemDefinition.cost = self.item_json["cost"]
        self.itemDefinition.lowalch = self.item_json["lowalch"]
        self.itemDefinition.highalch = self.item_json["highalch"]

    def determine_wiki_page(self):
        """Determine the OSRS Wiki page/url/name using the item name."""
        # Set the initial wiki_name property to the actual item name
        # This may change depending on the item lookup success/failure
        wiki_name = self.itemDefinition.name

        # PHASE ONE: Check if the item name is in the OSRS Wiki item dump using normalized name

        if str(self.itemDefinition.id) in self.normalized_names:
            self.logger.debug(">>> ITEM FOUND IN NORMALIZED")
            # Determine normalized wiki name using lookup
            normalized_name = self.normalized_names[str(self.itemDefinition.id)][1]
            # Set wiki URL and name
            wiki_url = normalized_name.replace(" ", "_")
            wiki_url = wiki_url.replace("'", "%27")
            wiki_url = wiki_url.replace("&", "%26")
            wiki_url = wiki_url.replace("+", "%2B")
            self.itemDefinition.url = f"https://oldschool.runescape.wiki/w/{wiki_url}"
            self.itemDefinition.wiki_name = normalized_name
            # Set item status code
            self.status_code = int(self.normalized_names[str(self.itemDefinition.id)][2])
            # Item name found in dump using normalization, return True
            return True

        # PHASE TWO: Check if the item name is in the OSRS Wiki item dump (no normalization)

        if wiki_name in self.wiki_text:
            self.logger.debug(">>> ITEM FOUND")
            # Set wiki URL and name
            wiki_url = self.itemDefinition.name.replace(" ", "_")
            wiki_url = wiki_url.replace("'", "%27")
            wiki_url = wiki_url.replace("&", "%26")
            wiki_url = wiki_url.replace("+", "%2B")
            self.itemDefinition.url = f"https://oldschool.runescape.wiki/w/{wiki_url}"
            self.itemDefinition.wiki_name = self.itemDefinition.name
            # Set item status code, try/except as it may not be in list
            try:
                self.status_code = int(self.normalized_names[str(self.itemDefinition.id)][2])
            except KeyError:
                self.status_code = 0  # Zero is no issue with item, direct lookup
            # Item name found in dump without normalization, return True
            return True

        # If we got this far, the wiki page was not found, return false
        self.logger.debug(">>> ITEM NOT FOUND")
        return False

    def extract_infobox(self):
        """Extract the primary properties and bonuses for the item."""
        # Set templates
        self.template_primary = None
        self.template_bonuses = None

        try:
            wiki_text_entry = self.wiki_text[self.itemDefinition.wiki_name]
            wikicode = mwparserfromhell.parse(wiki_text_entry)
        except KeyError:
            # The wiki_name was not found in the available dumped wikitext pages
            # Return false to indicate no wikitext was extracted
            self.logger.debug("extract_infobox: KeyError for self.wikitext")
            return False

        # Loop through templates in wikicode from wiki page
        # Then call Inforbox Item processing method
        templates = wikicode.filter_templates()
        for template in templates:
            template_name = template.name.strip()
            template_name = template_name.lower()
            if "infobox item" in template_name:
                self.template_primary = template
            if "infobox bonuses" in template_name:
                self.template_bonuses = template
            if "infobox construction" in template_name:
                self.template_primary = template
            if "infobox pet" in template_name:
                self.template_primary = template

        # If no template_primary was found, return false
        if not self.template_primary:
            self.logger.debug("extract_infobox: not self.template_primary")
            return False

        # If any equipable item, and no bonuses was found, return false
        if self.itemDefinition.equipable and not self.template_bonuses:
            self.logger.debug("extract_infobox: not self.template_bonuses")
            return False

        # If we got this far, return true
        return True

    def parse_primary_infobox(self):
        """Parse an actual Infobox template."""
        template = self.template_primary
        # Set defaults for versioned infoboxes
        is_versioned = False  # has multiple versions available
        self.current_version = None  # The version that matches the item
        version_count = 0  # the number of versions available

        # STAGE ONE: Determine if we have a versioned infobox, and the version count

        version_identifiers = ["version",
                               "name",
                               "itemname"]

        for version_identifier in version_identifiers:
            # Check if the infobox is versioned, and get a version count
            if version_count == 0:
                try:
                    template.get(version_identifier + "1").value
                    is_versioned = True
                    # Now, try to determine how many versions are present
                    i = 1
                    while i <= 20:  # Guessing max version number is 20
                        try:
                            template.get(version_identifier + "1").value
                            version_count += 1
                        except ValueError:
                            break
                        i += 1
                except ValueError:
                    pass

        # STAGE TWO: Match a versioned infobox to the item name

        if is_versioned:
            # Try determine
            for version_identifier in version_identifiers:
                try:
                    template.get(version_identifier + "1").value
                    i = 1
                    while i <= version_count:
                        versioned_name = version_identifier + str(i)
                        if self.itemDefinition.name == template.get(versioned_name).value.strip():
                            self.current_version = i
                        i += 1
                except ValueError:
                    pass

            self.logger.debug("NOTE: versioned infobox: %s" % self.current_version)

        if is_versioned and self.current_version is None:
            self.current_version = 1

        # WEIGHT: Determine the weight of an item ()
        weight = None
        if self.current_version is not None:
            key = "weight" + str(self.current_version)
            weight = self.extract_infobox_value(template, key)
        if weight is None:
            weight = self.extract_infobox_value(template, "weight")
        if weight is not None:
            self.itemDefinition.weight = infobox_cleaner.clean_weight(weight)

        # QUEST: Determine if item is associated with a quest ()
        quest = None
        if self.current_version is not None:
            key = "quest" + str(self.current_version)
            quest = self.extract_infobox_value(template, key)
        if quest is None:
            quest = self.extract_infobox_value(template, "quest")
        if quest is not None:
            self.itemDefinition.quest_item = infobox_cleaner.clean_quest(quest)

        # Determine the release date of an item ()
        release_date = None
        if self.current_version is not None:
            key = "release" + str(self.current_version)
            release_date = self.extract_infobox_value(template, key)
        if release_date is None:
            release_date = self.extract_infobox_value(template, "release")
        if release_date is not None:
            self.itemDefinition.release_date = infobox_cleaner.clean_release_date(release_date)

        # Determine if item has a store price ()
        store_price = None
        if self.current_version is not None:
            key = "store" + str(self.current_version)
            store_price = self.extract_infobox_value(template, key)
        if store_price is None:
            store_price = self.extract_infobox_value(template, "store")
        if store_price is not None:
            self.itemDefinition.store_price = infobox_cleaner.clean_store_price(store_price)

        # Determine if item has a store price ()
        seller = None
        if self.current_version is not None:
            key = "seller" + str(self.current_version)
            seller = self.extract_infobox_value(template, key)
        if seller is None:
            seller = self.extract_infobox_value(template, "seller")
        if seller is not None:
            self.itemDefinition.seller = infobox_cleaner.clean_seller(seller)

        # Determine the examine text of an item ()
        tradeable = None
        if self.current_version is not None:
            key = "tradeable" + str(self.current_version)
            tradeable = self.extract_infobox_value(template, key)
        if tradeable is None:
            tradeable = self.extract_infobox_value(template, "tradeable")
        if tradeable is not None:
            self.itemDefinition.tradeable = infobox_cleaner.clean_tradeable(tradeable)
        else:
            self.itemDefinition.tradeable = False

        # Determine the examine text of an item ()
        examine = None
        if self.current_version is not None:
            key = "examine" + str(self.current_version)
            examine = self.extract_infobox_value(template, key)
        if examine is None:
            examine = self.extract_infobox_value(template, "examine")
        if examine is not None:
            self.itemDefinition.examine = infobox_cleaner.clean_examine(examine, self.itemDefinition.name)
        else:
            # Being here means the extraction for "examine" failed
            key = "itemexamine" + str(self.current_version)
            examine = self.extract_infobox_value(template, key)
            if examine is None:
                examine = self.extract_infobox_value(template, "itemexamine")
            if examine is not None:
                self.itemDefinition.examine = infobox_cleaner.clean_examine(examine, self.itemDefinition.name)

        # Determine if item has a buy limit ()
        if not self.itemDefinition.tradeable:
            self.itemDefinition.buy_limit = None
        else:
            try:
                self.itemDefinition.buy_limit = int(self.buy_limits[self.itemDefinition.name])
                if self.itemDefinition.noted:
                    self.itemDefinition.buy_limit = None
            except KeyError:
                self.itemDefinition.buy_limit = None

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

    def extract_bonuses(self) -> bool:
        """Extract the infobox bonuses template from raw wikitext.

        :return: If the infobox bonuses template was extracted successfully or not.
        """
        # Extract Infobox Bonuses from wikitext
        try:
            wikicode = mwparserfromhell.parse(self.wiki_text[self.itemDefinition.wiki_name])
        except KeyError:
            return False
        templates = wikicode.filter_templates()
        for template in templates:
            if "infobox bonuses" in template.lower():
                extracted_infobox = self.parse_bonuses(template)
                if extracted_infobox:
                    return True

        return False

    def parse_bonuses(self, template: mwparserfromhell.nodes.template.Template) -> bool:
        """Parse the wiki text template and extract item bonus values from it.

        :param template: A mediawiki wiki text template.
        """
        self.itemDefinition.item_stats.attack_stab = self.clean_bonuses_value(template, "astab")
        self.itemDefinition.item_stats.attack_slash = self.clean_bonuses_value(template, "aslash")
        self.itemDefinition.item_stats.attack_crush = self.clean_bonuses_value(template, "acrush")
        self.itemDefinition.item_stats.attack_magic = self.clean_bonuses_value(template, "amagic")
        self.itemDefinition.item_stats.attack_ranged = self.clean_bonuses_value(template, "arange")
        self.itemDefinition.item_stats.defence_stab = self.clean_bonuses_value(template, "dstab")
        self.itemDefinition.item_stats.defence_slash = self.clean_bonuses_value(template, "dslash")
        self.itemDefinition.item_stats.defence_crush = self.clean_bonuses_value(template, "dcrush")
        self.itemDefinition.item_stats.defence_magic = self.clean_bonuses_value(template, "dmagic")
        self.itemDefinition.item_stats.defence_ranged = self.clean_bonuses_value(template, "drange")
        self.itemDefinition.item_stats.melee_strength = self.clean_bonuses_value(template, "str")
        self.itemDefinition.item_stats.ranged_strength = self.clean_bonuses_value(template, "rstr")
        self.itemDefinition.item_stats.magic_damage = self.clean_bonuses_value(template, "mdmg")
        self.itemDefinition.item_stats.prayer = self.clean_bonuses_value(template, "prayer")

        try:
            self.itemDefinition.item_equipment.slot = self.strip_infobox(template.get("slot").value)
            self.itemDefinition.item_equipment.slot = self.itemDefinition.item_equipment.slot.lower()
        except ValueError:
            self.itemDefinition.item_equipment.slot = None
            self.logger.critical("Could not determine equipable item slot")

        # If item is weapon, two-handed, or 2h determine attack speed
        if (self.itemDefinition.item_equipment.slot == "weapon" or
                self.itemDefinition.item_equipment.slot == "two-handed" or
                self.itemDefinition.item_equipment.slot == "2h"):
            try:
                self.itemDefinition.item_equipment.attack_speed = int(self.strip_infobox(template.get("aspeed").value))
            except ValueError:
                self.itemDefinition.item_equipment.attack_speed = None
                self.logger.critical("Could not determine equipable item attack speed")
        if self.itemDefinition.item_equipment.attack_speed == 0:
            self.itemDefinition.item_equipment.attack_speed = None

        # Fetch item skill requirements
        try:
            skill_reqs = self.skill_requirements[str(self.item_id)]
            self.itemDefinition.item_equipment.skill_reqs = skill_reqs
        except KeyError:
            self.itemDefinition.item_equipment.skill_reqs = None

        return True

    def clean_bonuses_value(self, template: mwparserfromhell.nodes.template.Template, prop: str):
        """Clean a item bonuses value extracted from a wiki template.

        :param template: A mediawiki wiki text template.
        :param prop: The key to query in the template.
        :return value: The extracted template value that has been int cast.
        """
        value = None

        # Try and get the versioned infobox value
        if self.current_version is not None:
            key = prop + str(self.current_version)
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

    def equipable_item_set_default(self):
        """Set a default item_stats and item_equipment object."""
        self.itemDefinition.item_stats.attack_stab = 0
        self.itemDefinition.item_stats.attack_slash = 0
        self.itemDefinition.item_stats.attack_crush = 0
        self.itemDefinition.item_stats.attack_magic = 0
        self.itemDefinition.item_stats.attack_ranged = 0
        self.itemDefinition.item_stats.defence_stab = 0
        self.itemDefinition.item_stats.defence_slash = 0
        self.itemDefinition.item_stats.defence_crush = 0
        self.itemDefinition.item_stats.defence_magic = 0
        self.itemDefinition.item_stats.defence_ranged = 0
        self.itemDefinition.item_stats.melee_strength = 0
        self.itemDefinition.item_stats.ranged_strength = 0
        self.itemDefinition.item_stats.magic_damage = 0
        self.itemDefinition.item_stats.prayer = 0

        self.itemDefinition.item_equipment.slot = None
        self.itemDefinition.item_equipment.attack_speed = None
        self.itemDefinition.item_equipment.skill_reqs = None

    def compare_json_files(self) -> bool:
        """Print the difference between this item object, and the item that exists in the database.

        :return changed: A boolean if the item is different, or not.
        """
        changed = False
        changes = dict()

        # Create JSON out object to compare
        current_json = self.itemDefinition.construct_json()

        # Try get existing entry (KeyError means it doesn't exist - aka a new item)
        try:
            existing_json = self.current_db[self.item_id]
        except KeyError:
            return changed

        for prop in self.properties:
            if current_json[prop] != existing_json[prop]:
                changed = True
                changes[prop] = [current_json[prop], existing_json[prop]]

                # Also check equipable
                if self.itemDefinition.equipable:
                    for stats_prop in self.stat_properties:
                        if current_json["bonuses"][stats_prop] != existing_json["bonuses"][stats_prop]:
                            changed = True
                            changes[stats_prop] = [current_json["bonuses"][stats_prop],
                                                   existing_json["bonuses"][stats_prop]]
                    for equipment_prop in self.equipment_properties:
                        if current_json["equipment"][equipment_prop] != existing_json["equipment"][equipment_prop]:
                            changed = True
                            changes[equipment_prop] = [current_json["equipment"][equipment_prop],
                                                       existing_json["equipment"][equipment_prop]]

        # Print any item changes
        if changed:
            print(f">>>>>>>>>>> id: {self.itemDefinition.id}\tname: {self.itemDefinition.name}")
            for prop in changes:
                print("+++ MISMATCH!:", prop)
                print("TYPES:", type(changes[prop][1]), type(changes[prop][0]))
                print("OLD: %r" % changes[prop][1])
                print("NEW: %r" % changes[prop][0])
            print()

        return changed
