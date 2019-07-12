"""
Author:  PH01L
Email:   phoil@osrsbox.com
Website: https://www.osrsbox.com

Description:
A module to ease parsing and extraction of data from an OSRS Wiki page that
is in raw wikitext format. A simple summary is provided below:

# Initialize the WikitextTemplateParser object, only need to pass raw wikitext
infobox_parser = WikitextTemplateParser(wikitext)

# Try to extract an infobox template, will return a boolean of success/failure
# You can pass:
# infobox item, infobox bonuses, infobox pet, infobox npx etc.
# The actual infobox template is stored in the object (infobox_parser.template)
has_infobox = infobox_parser.extract_infobox("infobox item")

# Determine if the extracted infobox is versioned, returns boolean
is_versioned = infobox_parser.determine_infobox_versions()

# Extract the item IDs from an infobox, including version support
# Returns a dictionary of item ID -> version number:
# For example: {12647: '1', 12654: '2'}
data = infobox_parser.extract_infobox_ids()

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
from typing import Union, List, Dict

import mwparserfromhell


class WikitextTemplateParser:
    def __init__(self, wikitext):
        self.wikitext = wikitext  # the raw wikitext
        self.template = None  # the extacted template
        self.is_versioned = False  # is the template representing multiple entities

        # Set specific wikitext infobox properties that can be versioned
        self.version_identifiers = {"id": 0,
                                    "version": 0,
                                    "name": 0,
                                    "itemid": 0}

        # Remove log, if it exists
        if os.path.exists("template_parser.log"):
            os.remove("template_parser.log")

        # Setup logging
        logging.basicConfig(filename="template_parser.log",
                            filemode='a',
                            level=logging.DEBUG)
        self.logger = logging.getLogger(__name__)
        self.logger.debug("\n>>> Starting processing...")

    def extract_infobox(self, template_type: str) -> bool:
        """Parse raw wikitext and extract a specified infobox.

        The OSRS Wiki stores structured information in a variety of different
        infobox templates structured using wikitext. This function parses the
        raw wikitext and extracts a wikitext template based on the template name
        provided as a paramater. Infobox example names include:

        `infobox item`: An infobox for item properties.
        `infobox bonuses`: An infobox for equipable item bonuses.

        A full list of all OSRS Wiki templates is available from:
        https://oldschool.runescape.wiki/w/RuneScape:Templates

        :param template_type: The type of infobox to extract.
        :return: A boolean representing sucessful processing.
        """
        try:
            wikicode = mwparserfromhell.parse(self.wikitext)
        except KeyError:
            # The wiki_name was not found in the available dumped wikitext pages
            # Return false to indicate no wikitext was extracted
            # TODO: This should catch a different error
            self.logger.debug("extract_infobox: KeyError for self.wikitext")
            return False

        # Loop through templates in wikicode from wiki page
        # Then call Inforbox Item processing method
        templates = wikicode.filter_templates()
        for template in templates:
            template_name = template.name.strip()
            template_name = template_name.lower()
            if template_type in template_name:
                self.template = template
                # Only find the first instance, so break
                break

        # If no template_primary was found, return false
        if not self.template:
            self.logger.debug("extract_infobox: Did not find a matching template.")
            return False

        # Print the raw wikitext template to the log
        self.logger.debug("extract_infobox: Found the following template.")
        self.logger.debug(f"\n{self.template}")

        # If we got this far, return true
        return True

    def determine_infobox_versions(self) -> bool:
        """Determine if the infobox template is versioned.

        Many OSRS Wiki infobox templates are versioned. This means that the infobox
        may represent multiple entities. For example, an `infobox item` may represent
        multiple items in different forms. This helper method will parse an infobox
        template and determine if multiple entites are discovered.

        :return: A boolean representing sucessful processing.
        """
        self.logger.debug("determine_infobox_versions: Checking if the infobox is versioned")
        # Loop through the different version identifiers
        for version_identifier in self.version_identifiers:
            self.logger.debug(f"determine_infobox_versions: Checking {version_identifier}")
            try:
                self.template.get(version_identifier + "1").value
                self.is_versioned = True
                break
            except ValueError:
                pass

        # If the infobox is not versioned, return False
        if not self.is_versioned:
            self.logger.debug("determine_infobox_versions: Infobox is NOT versioned...")
            return False
        else:
            self.logger.debug("determine_infobox_versions: Infobox is versioned...")

        # The infobox is versioned... continue processing
        # Try to determine the version counts for each version identifier
        self.logger.debug("determine_infobox_versions: Determine infobox version counts...")
        for version_identifier in self.version_identifiers:
            self.logger.debug(f"determine_infobox_versions: Counting {version_identifier}")
            i = 1
            while i <= 50:
                try:
                    self.template.get(version_identifier + str(i)).value
                    self.version_identifiers[version_identifier] += 1
                except ValueError:
                    pass
                i += 1

        # Infobox versioning completed, log results
        self.logger.debug("determine_infobox_versions: Infobox version results:")
        self.logger.debug(f"    {self.version_identifiers}")

        # Processing finished
        return True

    def extract_infobox_value(self, key: str) -> str:
        """Helper method to extract a value from a template using a specified key.

        This helper method is a simple solution to repeatedly try to fetch a specific
        entry from a wiki text template (a mwparserfromhell template object).

        :param key: The key to query in the template.
        :return: The extracted template value based on supplied key.
        """
        value = None
        try:
            value = self.template.get(key).value
            value = value.strip()
            return value
        except ValueError:
            return value

    def extract_infobox_id(self, version: str) -> str:
        """Helper method to extract an ID from a template using harcoded ID keys.

        This helper method is a solution to query an infobox template for
        a unique ID number. The keys used are:
        `id`: Query template using only the string `id`.
        `id + version`: Query template using the string `id` including the `version` number.
        `itemid`: Query template using only the string `itemid`.
        `itemid + version`: Query template using the string `itemid` including the `version` number.

        :param version: The number, as a string, to represent a versioned infobox.
        :return: The extracted template ID value (can be a comma-seperated string).
        """
        value = None
        id_key = "id" + version
        try:
            value = self.template.get(id_key).value
            value = value.strip()
            return value
        except ValueError:
            itemid_key = "itemid" + version
            try:
                value = self.template.get(itemid_key).value
                value = value.strip()
                return value
            except ValueError:
                return value

    def split_infobox_id_string(self, id_string: str) -> List:
        """Helper method to split a comma-separated string of item IDs.

        Some item ID property values are comma-seperated. This helper method
        splits the string and returns a list of IDs. If there is only one
        item ID, the method creates and returns the single value in a list.
        For example:
        2345,3456 outputs [2345, 3456]
        34 outputs [34]

        :param id_string: A string of potentially comma-sererated item IDs
        :return: List of item IDs
        """
        id_list = list()
        if "," in id_string:
            id_list = id_string.split(",")
        else:
            id_list.append(id_string)
        return id_list

    def extract_infobox_ids(self) -> Dict:
        """Extracts the item ID from a versione, or un-versioned Infobox.

        This method extracts item IDs from a versined, or un-versioned, infobox
        template from the OSRS Wiki data. The data returned is a dictionary mapping:
        item_id -> version_number

        Versioned example: the Kalphite princess pet item has two versions, crawling
        or airbourne. This method parses an already extracted `infobox pet` template
        an extracts the IDs associated with each item, including the infobox version
        number:
        id: 12647 is the crawling version, that uses version 1 in the infobox
        id: 12654 is the airnourne version, that uses version 2 in the infobox
        Returned data: {12647: '1', 12654: '2'}

        Un-versioned example: Pet k'ril tsutsaroth has only one version.
        id: 12652
        Returned data: {12652: ""}
        The empty string indicates that no addition to the `id` property is needed
        to extract the data correctly, as the infobox is not versioned.

        :return: A dictionary mapping item ID to version number.
        """
        item_id_to_version_number = dict()
        if self.is_versioned:
            count = self.version_identifiers["id"]
            if count == 0:
                count = self.version_identifiers["itemid"]
            i = 1
            while i <= count:
                id = self.extract_infobox_id(str(i))  # Pass string cast version number
                ids = self.split_infobox_id_string(id)
                for id in ids:
                    id = self.try_int_cast(id)
                    if id:
                        item_id_to_version_number[id] = str(i)
                i += 1
        else:
            id = self.extract_infobox_id("")  # Pass empty string, not versioned
            ids = self.split_infobox_id_string(id)
            for id in ids:
                id = self.try_int_cast(id)
                if id:
                    item_id_to_version_number[id] = ""

        return item_id_to_version_number

    def try_int_cast(self, value: str) -> Union[int, None]:
        """Helper method to try int cast a string.

        :param value: A value to try int cast.
        :return: Either an integer or None
        """
        try:
            return int(value)
        except ValueError:
            return None
