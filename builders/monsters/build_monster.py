"""
Author:  PH01L
Email:   phoil@osrsbox.com
Website: https://www.osrsbox.com

Description:
Build a monster given OSRS cache, wiki and custom data.

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
from pathlib import Path
from datetime import datetime
from datetime import timezone

import mwparserfromhell
from deepdiff import DeepDiff

import config
import validator
from builders.monsters import infobox_cleaner
from scripts.wiki.wikitext_parser import WikitextTemplateParser
from osrsbox.monsters_api.monster_properties import MonsterProperties


class BuildMonster:
    def __init__(self, **kwargs):
        # ID number to process
        self.monster_id = kwargs["monster_id"]
        # Raw cache data for all monsters
        self.all_monster_cache_data = kwargs["all_monster_cache_data"]
        # The existing monster database contents
        self.all_db_monsters = kwargs["all_db_monsters"]
        # Raw data dump from OSRS Wiki
        self.all_wikitext_raw = kwargs["all_wikitext_raw"]
        # Processed wikitext for all monsters
        self.all_wikitext_processed = kwargs["all_wikitext_processed"]
        # Processed monster drops
        self.monsters_drops = kwargs["monsters_drops"]
        # The monster schema
        self.schema_data = kwargs["schema_data"]
        # A list of already known (processed) monsters
        self.known_monsters = kwargs["known_monsters"]
        # Specify verbosity
        self.verbose = kwargs["verbose"]

        # For this monster instance, create dictionary for property storage
        self.monster_dict = dict()
        # The page name the wikitext is from
        self.wiki_page_name = None
        # The version used on the wikitext page
        self.infobox_version_number = None
        # Used if the item is special (invalid, normalized etc.)
        self.status = None

    def preprocessing(self):
        """Preprocess an monster, and set important object variables.

        This function preprocesses every monster dumped from the OSRS cache. Various
        properties are set to help further processing. MORE."""
        # Set monster ID variables
        self.monster_id_int = int(self.monster_id)  # Monster ID number as an integer
        self.monster_id_str = str(self.monster_id)  # Monster ID number as a string

        # Load monster dictionary of cache data based on monster ID
        # This raw cache data is the baseline information about the specific monster
        # and can be considered 100% correct and available for every monster
        self.monster_cache_data = self.all_monster_cache_data[self.monster_id_str]

        # Set monster name variable (directly from the cache dump)
        self.monster_name = self.monster_cache_data["name"]

        # Log and print monster
        if self.verbose:
            print(f"======================= {self.monster_id_str} {self.monster_name}")

        # Set all variables to None (for invalid monsters)
        self.monster_wikitext = None
        self.wikitext_found_using = None
        self.has_infobox = False

        # Try to find the wiki data using direct ID number search
        if self.all_wikitext_processed.get(self.monster_id_str, None):
            self.monster_wikitext = self.all_wikitext_processed.get(self.monster_id_str, None)
            self.wikitext_found_using = "id"

        # Try to find the wiki data using direct name search
        elif self.all_wikitext_raw.get(self.monster_name, None):
            self.monster_wikitext = self.all_wikitext_raw.get(self.monster_name, None)
            self.wikitext_found_using = "name"

        # If there is no wikitext, and the monster is valid, raise a critical error
        if not self.monster_wikitext:
            return False

        # Parse the infobox monster
        infobox_parser = WikitextTemplateParser(self.monster_wikitext)

        # Try extract infobox for monster
        self.has_infobox = infobox_parser.extract_infobox("infobox monster")
        if not self.has_infobox:
            return False

        self.is_versioned = infobox_parser.determine_infobox_versions()
        self.versioned_ids = infobox_parser.extract_infobox_ids()

        # Set the infobox version number, default to empty string (no version number)
        try:
            if self.versioned_ids:
                self.infobox_version_number = self.versioned_ids[self.monster_id_int]
        except KeyError:
            if self.is_versioned:
                self.infobox_version_number = "1"
            else:
                self.infobox_version_number = ""

        # Set the template
        self.template = infobox_parser.template

        return True

    def populate_monster(self):
        """Populate a monster after preprocessing it.

        This is called for every monster in the OSRS cache dump that has a wiki page.
        Start by populating the raw metadata from the cache. Then use the wiki data
        to populate more properties.
        """
        self.populate_from_cache_data()
        self.populate_monster_properties_from_wiki_data()

    def populate_from_cache_data(self):
        """Populate a monster using raw cache data.

        This function takes the raw OSRS cache data for the specific monster and loads
        all available properties (that are extracted from the cache)."""
        # Log, then populate cache properties
        self.monster_dict["id"] = self.monster_cache_data["id"]
        self.monster_dict["name"] = self.monster_cache_data["name"]
        self.monster_dict["combat_level"] = self.monster_cache_data["combatLevel"]
        self.monster_dict["size"] = self.monster_cache_data["size"]

    def populate_monster_properties_from_wiki_data(self):
        """Populate item data from a OSRS Wiki Infobox Item template."""
        # STAGE ONE: Determine then set the wiki_name and wiki_url

        # Manually set OSRS Wiki name
        if self.wikitext_found_using not in ["id"]:
            # Monster found in wiki by ID, cache name is the best option
            wiki_page_name = self.monster_name
        else:
            # Monster found using direct cache name lookup on wiki page names,
            # So use wiki page name in the monster_wikitext array
            wiki_page_name = self.monster_wikitext[0]

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

        self.monster_dict["wiki_name"] = wiki_name

        # Set the wiki_url property
        if wiki_versioned_name is not None:
            wiki_url = wiki_page_name + "#" + wiki_versioned_name
        else:
            wiki_url = wiki_page_name

        wiki_url = wiki_url.replace(" ", "_")
        self.monster_dict["wiki_url"] = "https://oldschool.runescape.wiki/w/" + wiki_url

        # STAGE TWO: Extract, process and set monster properties from the infobox template

        # Initialize a dictionary that maps proj_name -> prop_name
        # proj_name is used in this project
        # prop_name is used by the OSRS Wiki
        monster_properties = {"members": "members",
                              "release_date": "release",
                              "hitpoints": "hitpoints",
                              "max_hit": "max hit",
                              "attack_type": "attack style",
                              "attack_speed": "attack speed",
                              "aggressive": "aggressive",
                              "poisonous": "poisonous",
                              "venomous": "poisonous",
                              "immune_poison": "immunepoison",
                              "immune_venom": "immunevenom",
                              "attributes": "attributes",
                              "category": "cat",
                              "slayer_level": "slaylvl",
                              "slayer_xp": "slayxp",
                              "examine": "examine"}

        # Loop each of the combat bonuses and populate
        for proj_name, prop_name in monster_properties.items():
            value = None
            if self.infobox_version_number is not None:
                key = prop_name + str(self.infobox_version_number)
                value = self.extract_infobox_value(self.template, key)

            if value is None:
                value = self.extract_infobox_value(self.template, prop_name)

            self.monster_dict[proj_name] = infobox_cleaner.caller(value, proj_name)

            if value is None:
                self.monster_dict["incomplete"] = True

        # Set slayer level to one, if slayer xp is given and
        # slayer level is None
        if self.monster_dict["slayer_xp"]:
            if self.monster_dict["slayer_level"] is None:
                self.monster_dict["slayer_level"] = 1

        # SLAYER MONSTER: Determine if the monster can be a slayer task
        if self.monster_dict["slayer_xp"]:
            self.monster_dict["slayer_monster"] = True
        else:
            self.monster_dict["slayer_monster"] = False

        # SLAYER MASTERS: Determine the slayer masters
        if self.monster_dict["slayer_monster"]:
            slayer_masters = None
            if self.infobox_version_number is not None:
                key = "assignedby" + str(self.infobox_version_number)
                slayer_masters = self.extract_infobox_value(self.template, key)
            if slayer_masters is None:
                slayer_masters = self.extract_infobox_value(self.template, "assignedby")
            if slayer_masters is not None:
                self.monster_dict["slayer_masters"] = infobox_cleaner.slayer_masters(slayer_masters)
            else:
                self.monster_dict["slayer_masters"] = list()
                self.monster_dict["incomplete"] = True
        else:
            self.monster_dict["slayer_masters"] = list()

        # MONSTER COMBAT BONUSES: Determine stats of the monster

        # Initialize a dictionary that maps database_name -> property_name
        # The database_name is used in this project
        # The property_name is used by the OSRS Wiki
        combat_bonuses = {"attack_level": "att",
                          "strength_level": "str",
                          "defence_level": "def",
                          "magic_level": "mage",
                          "ranged_level": "range",
                          "attack_bonus": "attbns",
                          "strength_bonus": "strbns",
                          "attack_magic": "amagic",
                          "magic_bonus": "mbns",
                          "attack_ranged": "arange",
                          "ranged_bonus": "rngbns",
                          "defence_stab": "dstab",
                          "defence_slash": "dslash",
                          "defence_crush": "dcrush",
                          "defence_magic": "dmagic",
                          "defence_ranged": "drange",
                          }

        # Loop each of the combat bonuses and populate
        for database_name, property_name in combat_bonuses.items():
            value = None
            if self.infobox_version_number is not None:
                key = property_name + str(self.infobox_version_number)
                value = self.extract_infobox_value(self.template, key)
            if value is None:
                value = self.extract_infobox_value(self.template, property_name)
            if value is not None:
                self.monster_dict[database_name] = infobox_cleaner.stats(value)
            else:
                self.monster_dict[database_name] = 0
                self.monster_dict["incomplete"] = True

        # We finished processing, set incomplete to false if not true
        if not self.monster_dict.get("incomplete"):
            self.monster_dict["incomplete"] = False

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

    def check_duplicate_monster(self) -> MonsterProperties:
        """Determine if this is a duplicate monster.

        :return: A MonsterProperties object.
        """
        # Start by setting the duplicate property to False
        self.monster_dict["duplicate"] = False

        # Check/set last update
        last_update = self.all_db_monsters.get(self.monster_id, None)
        if last_update:
            self.monster_dict["last_updated"] = self.all_db_monsters[self.monster_id]["last_updated"]
        else:
            self.monster_dict["last_updated"] = datetime.now(timezone.utc).strftime("%Y-%m-%d")

        # Create an MonsterProperties object
        monster_properties = MonsterProperties(**self.monster_dict)

        # Set the monster properties that we want to compare
        correlation_properties = {
            "wiki_name": False,
            "combat_level": False,
            "members": False
        }

        # Loop the list of currently (already processed) monsters
        for known_monster in self.known_monsters:
            # Do a quick name check before deeper inspection
            if monster_properties.name != known_monster.name:
                continue

            # If the cache names are equal, do further inspection
            for cprop in correlation_properties:
                if getattr(monster_properties, cprop) == getattr(known_monster, cprop):
                    correlation_properties[cprop] = True

            # Check is all values in correlation properties are True
            correlation_result = all(value is True for value in correlation_properties.values())
            if correlation_result:
                self.monster_dict["duplicate"] = True

        return monster_properties

    def populate_monster_drops(self):
        """Set the monster drops from preprocessed data."""
        try:
            self.monster_dict["drops"] = self.monsters_drops[self.monster_id]
        except KeyError:
            self.monster_dict["drops"] = []

    def compare_new_vs_old_monster(self):
        """Diff this monster and the monster that exists in the database."""
        # Create JSON out object to compare
        self.monster_properties = MonsterProperties(**self.monster_dict)
        current_json = self.monster_properties.construct_json()

        # Try get existing entry (KeyError means it doesn't exist - aka a new monster)
        try:
            existing_json = self.all_db_monsters[self.monster_id]
        except KeyError:
            print(f">>> compare_json_files: NEW MONSTER: {self.monster_properties.id}")
            print(current_json)
            self.monster_dict["last_updated"] = datetime.now(timezone.utc).strftime("%Y-%m-%d")
            return

        # Quick check of eqaulity, return if properties and drops are the same
        if current_json == existing_json:
            self.monster_dict["last_updated"] = self.all_db_monsters[self.monster_id]["last_updated"]
            return

        # Print a header for the changed monster
        print(f">>> compare_json_files: CHANGED MONSTER: {self.monster_properties.id}: {self.monster_properties.name}")

        # First check the base properties
        ddiff_props = DeepDiff(existing_json, current_json, ignore_order=True)
        if ddiff_props:
            print(ddiff_props)

        self.monster_dict["last_updated"] = datetime.now(timezone.utc).strftime("%Y-%m-%d")

    def export_monster_to_json(self):
        """Export monster to JSON, if requested."""
        self.monster_properties = MonsterProperties(**self.monster_dict)
        output_dir = Path(config.DOCS_PATH, "monsters-json")
        self.monster_properties.export_json(True, output_dir)

    def validate_monster(self):
        """Use the schema-monsters.json file to validate the populated monster."""
        # Create JSON out object to validate
        self.monster_properties = MonsterProperties(**self.monster_dict)
        current_json = self.monster_properties.construct_json()

        # Validate object with schema attached
        v = validator.MyValidator(self.schema_data)
        v.validate(current_json)

        # Print any validation errors
        if v.errors:
            print(v.errors)
            exit(1)

        assert v.validate(current_json)
