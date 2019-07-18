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

import json
import logging
from pathlib import Path

import mwparserfromhell

import config
from monsters_builder import infobox_cleaner
from osrsbox.monsters_api.monster_definition import MonsterDefinition
from osrsbox.monsters_api.monster_drop import MonsterDrop
from extraction_tools_wiki.wikitext_parser import WikitextTemplateParser
from extraction_tools_wiki.wikitext_parser import WikitextTemplatesParser

class BuildMonster:
    def __init__(self, monster_id, data):
        # Input monster ID number
        self.monster_id = monster_id

        # Handle dict import
        self.cache_name = data["cache_name"]
        self.wiki_name = data["wiki_name"]
        self.wiki_text = data["wiki_text"]
        self.monster_template = data["template"]
        self.infobox_version = data["infobox_version"]
        self.cache_combat_level = data["cache_combat_level"]

        # For this monster, create dictionary for property storage
        self.monster_dict = dict()

        # For this monster, create a empty list for drops
        self.drops = list()

        # Setup logging
        logging.basicConfig(filename="builder.log",
                            filemode='a',
                            level=logging.DEBUG)
        self.logger = logging.getLogger(__name__)

        self.monster_definition = MonsterDefinition()

    def populate(self):
        """The primary entry and monster object population function."""
        # Start section in logger
        self.logger.debug("============================================ START")
        self.logger.debug(f"monster_id: {self.monster_id}")
        # print(f"monster_id: {self.monster_id}, wiki_name: {self.wiki_name}")

        # STAGE ONE: INSERT HARD CODES VARS
        self.monster_dict["id"] = self.monster_id
        self.monster_dict["cache_name"] = self.cache_name
        self.monster_dict["wiki_name"] = self.wiki_name

        self.logger.debug(self.monster_template.encode("utf-8"))

        # STAGE TWO: PARSE THE TEMPLATE
        self.parse_monster_infobox_properties()
        self.parse_monster_infobox_stats()

        # STAGE THREE: PARSE THE DROPS
        self.parse_monster_drops()

        # This should not be here, but simplifies testing and passing flake8 check
        self.logger.debug(json.dumps(self.monster_dict, indent=4))

        # Populate the dataclass
        for k, v in self.monster_dict.items():
            setattr(self.monster_definition, k, v)

        # Actually output a JSON file, comment out for testing
        output_dir = Path(config.DOCS_PATH / "monsters-json" / "")
        self.monster_definition.export_json(True, output_dir)

    def extract_infobox(self):
        """Extract the templates in the provided wikitext for the monster."""
        # Set templates
        self.templates = list()  # List of templates from wikitext

        wiki_code = mwparserfromhell.parse(self.wiki_text)

        # Loop through templates in wikicode from wiki page
        # Then call Inforbox Item processing method
        templates = wiki_code.filter_templates()
        for template in templates:
            template_name = template.name.strip()
            template_name = template_name.lower()
            print(template_name)
            if "infobox monster" in template_name:
                self.templates.append(template)
            if "dropsline" in template_name:
                print("MEOWMEOWMEOW")

        # If no templates were found, return false
        if not self.templates:
            self.logger.debug("extract_infobox: not self.templates")
            return False

        self.logger.debug("extract_infobox: FOUND self.templates")
        self.logger.debug(self.templates)

        # If we got this far, return true
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

    def parse_monster_infobox_properties(self):
        """Parse an actual Infobox monster template."""
        # print(f"monster_id: {self.monster_id}, wiki_name: {self.wiki_name}, version: {self.infobox_version}")

        # If an non-versioned infobox (0), set to empty string
        if self.infobox_version == 0:
            self.infobox_version = ""

        # STAGE ONE: Start extracting regular monster properties

        # MEMBERS: Determine the members status of a monster (tested: False)
        key = "members" + str(self.infobox_version)
        # Try fecth using version number (e.g., id1, id2 - replace id with key name)
        members = self.extract_infobox_value(self.monster_template, key)
        if members is None:
            members = self.extract_infobox_value(self.monster_template, "members")
        # Clean and add to dict
        self.monster_dict["members"] = infobox_cleaner.clean_boolean(members)
        # print(self.monster_dict["members"])

        # RELEASE_DATE: Determine the release date of a monster (tested: False)
        key = "release" + str(self.infobox_version)
        # Try fecth using version number (e.g., id1, id2 - replace id with key name)
        release_date = self.extract_infobox_value(self.monster_template, key)
        if release_date is None:
            release_date = self.extract_infobox_value(self.monster_template, "release")
        # Clean and add to dict
        self.monster_dict["release_date"] = infobox_cleaner.clean_release_date(release_date)
        # print(self.monster_dict["release_date"])

        # COMBAT_LEVEL: Determine the combat level of a monster (tested: False)
        key = "combat" + str(self.infobox_version)
        # Try fecth using version number (e.g., id1, id2 - replace id with key name)
        combat_level = self.extract_infobox_value(self.monster_template, key)
        if combat_level is None:
            combat_level = self.extract_infobox_value(self.monster_template, "combat")
        # Clean and add to dict
        self.monster_dict["combat_level"] = infobox_cleaner.clean_combat_level(combat_level)
        # print(self.monster_dict["combat"])
        # print(self.cache_combat_level)

        # CODE BLOCK TO DETERMINE COMBAT LEVEL DIFFERENCES BETWEEN CACHE AND OSRS WIKI
        # if self.monster_dict["combat"]:
        #     if not int(self.monster_dict["combat"]) == int(self.cache_combat_level):
        #         print(f'{self.monster_id},{self.wiki_name},{self.monster_dict["combat"]},{self.cache_combat_level}')
        # else:
        #     if not int(self.monster_dict["combat"]) == int(self.cache_combat_level):
        #         print(f'{self.monster_id},{self.wiki_name},{self.monster_dict["combat"]},{self.cache_combat_level}')

        # HIT_POINTS: Determine the hitpoints of a monster (tested: False)
        key = "hitpoints" + str(self.infobox_version)
        # Try fecth using version number (e.g., id1, id2 - replace id with key name)
        hit_points = self.extract_infobox_value(self.monster_template, key)
        if hit_points is None:
            hit_points = self.extract_infobox_value(self.monster_template, "hitpoints")
        # Clean and add to dict
        self.monster_dict["hit_points"] = infobox_cleaner.clean_hitpoints(hit_points)

        # TODO: max hit
        # TODO: attack type
        # TODO: attack speed

        # AGGRESSIVE: Determine the aggressive property of a monster (tested: False)
        key = "aggressive" + str(self.infobox_version)
        # Try fecth using version number (e.g., id1, id2 - replace id with key name)
        aggressive = self.extract_infobox_value(self.monster_template, key)
        if aggressive is None:
            aggressive = self.extract_infobox_value(self.monster_template, "aggressive")
        # Clean and add to dict
        self.monster_dict["aggressive"] = infobox_cleaner.clean_boolean(aggressive)

        # POISONOUS: Determine the poisonous property of a monster (tested: False)
        key = "poisonous" + str(self.infobox_version)
        # Try fecth using version number (e.g., id1, id2 - replace id with key name)
        poisonous = self.extract_infobox_value(self.monster_template, key)
        if poisonous is None:
            poisonous = self.extract_infobox_value(self.monster_template, "poisonous")
        # Clean and add to dict
        self.monster_dict["poisonous"] = infobox_cleaner.clean_boolean(poisonous)

        # IMMUNE_POISON: Determine the immunity to poison property of a monster (tested: False)
        key = "immunepoison" + str(self.infobox_version)
        # Try fecth using version number (e.g., id1, id2 - replace id with key name)
        immune_poison = self.extract_infobox_value(self.monster_template, key)
        if immune_poison is None:
            immune_poison = self.extract_infobox_value(self.monster_template, "immunepoison")
        # Clean and add to dict
        self.monster_dict["immune_poison"] = infobox_cleaner.clean_boolean(immune_poison)

        # IMMUNE_VENOM: Determine the immunity to venon property of a monster (tested: False)
        key = "immunevenom" + str(self.infobox_version)
        # Try fecth using version number (e.g., id1, id2 - replace id with key name)
        immune_venom = self.extract_infobox_value(self.monster_template, key)
        if immune_venom is None:
            immune_venom = self.extract_infobox_value(self.monster_template, "immunevenom")
        # Clean and add to dict
        self.monster_dict["immune_venom"] = infobox_cleaner.clean_boolean(immune_venom)

        # TODO: weakness
        # TODO: slayer_level
        # TODO: slayer_xp
        # TODO: examine
        # TODO: url

    def parse_monster_infobox_stats(self) -> bool:
        """Parse the wiki text template and extract item bonus values from it."""
        self.monster_dict["attack_level"] = self.clean_stats_value("att")
        self.monster_dict["strength_level"] = self.clean_stats_value("str")
        self.monster_dict["defence_level"] = self.clean_stats_value("def")
        self.monster_dict["magic_level"] = self.clean_stats_value("mage")
        self.monster_dict["ranged_level"] = self.clean_stats_value("range")

        self.monster_dict["attack_stab"] = self.clean_stats_value("astab")
        self.monster_dict["attack_slash"] = self.clean_stats_value("aslash")
        self.monster_dict["attack_crush"] = self.clean_stats_value("acrush")
        self.monster_dict["attack_magic"] = self.clean_stats_value("amagic")
        self.monster_dict["attack_ranged"] = self.clean_stats_value("arange")

        self.monster_dict["defence_stab"] = self.clean_stats_value("dstab")
        self.monster_dict["defence_slash"] = self.clean_stats_value("dslash")
        self.monster_dict["defence_crush"] = self.clean_stats_value("dcrush")
        self.monster_dict["defence_magic"] = self.clean_stats_value("dmagic")
        self.monster_dict["defence_ranged"] = self.clean_stats_value("drange")

        self.monster_dict["attack_accuracy"] = self.clean_stats_value("attbns")
        self.monster_dict["melee_strength"] = self.clean_stats_value("strbns")
        self.monster_dict["ranged_strength"] = self.clean_stats_value("rngbns")
        self.monster_dict["magic_damage"] = self.clean_stats_value("mbns")

        return True

    def parse_monster_drops(self):
        infobox_parser = WikitextTemplatesParser(self.wiki_text)
        self.drops_templates = infobox_parser.extract_infoboxes("dropsline")

        print(self.drops_templates)

        for template in infobox_parser.templates:
            print(template)

        for template in infobox_parser.templates:
            drop_dict = {
                "id": None,
                "name": None,
                "quantity": None,
                "rarity": None,
                "drop_requirements": None
            }
            print(template)
            name = str(template.get("Name").value)
            quantity = str(template.get("Quantity").value)
            rarity = str(template.get("Rarity").value)
            # drop_requirements = template.get("Raritynotes").value
            drop_dict = {
                "id": None,
                "name": name,
                "quantity": quantity,
                "rarity": rarity,
                "drop_requirements": None
            }
            print(drop_dict)
            self.drops.append(drop_dict)

        self.monster_dict["drops"] = self.drops

    def clean_stats_value(self, prop: str):
        """Clean a item bonuses value extracted from a wiki template.

        :param prop: The key to query in the template.
        :return value: The extracted template value that has been int cast.
        """
        # Try and get the versioned infobox value
        key = prop + str(self.infobox_version)
        value = self.extract_infobox_value(self.monster_template, key)

        # If unsuccessful, try and get the normal infoxbox value
        if value is None:
            value = self.extract_infobox_value(self.monster_template, prop)

        if value:
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
            self.logger.debug(f"STATS ISSUE: ID: {self.monster_id}, "
                              f"WIKI: {self.wiki_name}, "
                              f"PROP: {prop}, "
                              f"VERSION: {self.infobox_version}")

        return value
