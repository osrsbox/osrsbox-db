"""
Author:  PH01L
Email:   phoil@osrsbox.com
Website: https://www.osrsbox.com

Description:
A module to ease parsing and extraction of data from a single OSRS Wiki page,
or multiple wiki pages (e.g., an API data dump).

This module has multiple helpers methods, as well as classes. A brief summary
for each major task is provided below:

1) extract_wikitext_template: A function to extract a template (usually an infobox)
from raw wikitext. Example usage:
    extracted_templates = extract_wikitext_template(wikitext, "infobox item")
Returns a list of extracted templates, in mwparserfromhell format

2) WikitextIDParser: A class to parse in an OSRS Wiki data dump and extract the
ID numbers from a user specified OSRS Wiki data dump. Example usage:
    wiki_text_file_path = Path("extract_page_text_items.json")
    template_names = ["infobox item", "infobox pet"]
    wiki_data_ids = WikitextIDParser(wiki_text_file_path, template_names)
Makes two accessible dictionaries:
    wiki_data_ids.item_id_to_version_number
    wiki_data_ids.item_id_to_wikitext

3) WikitextTemplateParser: A class to ease processing of wikitext templates. You
can have an already extracted mwparserfromhell template (most likely an infobox),
or extract the template on the fly. Example usage to load:
    infobox_parser = WikitextTemplateParser(wikitext)
If you have an already extracted template, add it to the class:
    infobox_parser.template = <some-template-object>
Otherwise you can try to extract an infobox template, will return a boolean of
success/failure. Make sure to pass a name (infobox item, infobox bonuses,
infobox pet).

Example usage:
    has_infobox = infobox_parser.extract_infobox("infobox item")
Determine if the extracted infobox is versioned, returns boolean:
    is_versioned = infobox_parser.determine_infobox_versions()
Extract the item IDs from an infobox, including version support. Returns a dictionary
of item ID -> version number. For example: {12647: '1', 12654: '2'}
    versioned_ids = infobox_parser.extract_infobox_ids()

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
import json
from pathlib import Path
from typing import Union, List, Dict

import mwparserfromhell


def extract_wikitext_template(wikitext: str, template_type: str, multiple: bool = True) -> List:
    """Parse raw wikitext and extract a specified template.

    The OSRS Wiki stores structured information in a variety of different
    infobox templates structured using wikitext. This function parses the
    raw wikitext and extracts a wikitext template/s based on the template name
    provided as a paramater. Infobox example names include:

    `infobox item`: An infobox for item properties.
    `infobox bonuses`: An infobox for equipable item bonuses.

    A full list of all OSRS Wiki templates is available from:
    https://oldschool.runescape.wiki/w/RuneScape:Templates

    :param wikitext: The raw wikitext.
    :param template_type: The type of infobox to extract.
    :param multiple: whether or not to extract multiple templates, default is True.
    :return: A list of mwpaserfromhell templates.
    """
    templates = list()

    try:
        wikicode = mwparserfromhell.parse(wikitext)
    except KeyError:
        # The wiki_name was not found in the available dumped wikitext pages
        # Return the empty list to indicate no templates were extracted
        return templates

    # Loop through templates in wikicode from wiki page...
    filtered_templates = wikicode.filter_templates()
    for template in filtered_templates:
        template_name = template.name.strip()
        template_name = template_name.lower()
        if template_type in template_name:
            templates.append(template)
            if not multiple:
                # Only find the first instance, so return now
                return templates

    # Return the list of extracted templates
    return templates


class WikitextIDParser:
    def __init__(self, wikitext_file_path: Path, template_names: List):
        self.wikitext_file_path = wikitext_file_path  # the raw wikitext dump
        self.template_names = template_names  # The infobox name (e.g., infobox item, infobox monster)
        self.item_id_to_wikitext = dict()  # Maps ID to wikitext (instead of name)
        self.item_id_to_version_number = dict()  # Maps ID to template version
        self.item_id_to_wiki_name = dict()  # Maps ID to original wiki page name

    def process_osrswiki_data_dump(self):
        """Process a raw OSRS Wiki and map IDs.

        The OSRS Wiki categorizes wiki pages using the page name. Sometimes
        it is highly useful to extract the ID numbers on the OSRS Wiki page
        dump and map the ID to the infobox/template version number and the
        raw wikitext.
        """
        # Read in the wiki text data dump
        with open(self.wikitext_file_path) as wikitext_file:
            wikitext_dump = json.load(wikitext_file)

        # Loop all items in the OSRS Wiki data dump
        for name, wikitext in wikitext_dump.items():
            # Loop the list of proivided infobox template names
            for template_name in self.template_names:
                # Initialize the wikitext template parser
                infobox_parser = WikitextTemplateParser(wikitext)
                has_infobox = infobox_parser.extract_infobox(template_name)
                if has_infobox:
                    infobox_parser.determine_infobox_versions()
                    versioned_ids = infobox_parser.extract_infobox_ids()
                    if not versioned_ids:
                        continue
                    for id, version_number in versioned_ids.items():
                        self.item_id_to_version_number[id] = version_number
                        self.item_id_to_wikitext[id] = wikitext
                        self.item_id_to_wiki_name[id] = name


class WikitextTemplateParser:
    def __init__(self, wikitext):
        self.wikitext = wikitext  # the raw wikitext
        self.template = None  # the extacted template
        self.is_versioned = False  # is the template representing multiple entities

        # Set specific wikitext infobox properties that can be versioned
        self.version_identifiers = {"id": 0,
                                    "name": 0,
                                    "itemid": 0}

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

        NOTE: This function will only extract the first occurance on the requested
        template. If there are multiple templates, only the first is used. This is
        usually fine, as there is only one infobox with a unique name per page.

        :param template_type: The type of infobox to extract.
        :return: A boolean representing sucessful processing.
        """
        try:
            wikicode = mwparserfromhell.parse(self.wikitext)
        except KeyError:
            # The wiki_name was not found in the available dumped wikitext pages
            # Return false to indicate no wikitext was extracted
            # TODO: This should catch a different error
            return False

        # Loop through templates in wikicode from wiki page
        # Then call Infobox Item processing method
        filtered_templates = wikicode.filter_templates()
        for template in filtered_templates:
            template_name = template.name.strip()
            template_name = template_name.lower()
            if template_type in template_name:
                self.template = template
                # Only find the first instance, so break
                break

        # If no template_primary was found, return false
        if not self.template:
            return False

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
        # Loop through the different version identifiers
        for version_identifier in self.version_identifiers:
            try:
                self.template.get(version_identifier + "1").value
                self.is_versioned = True
                break
            except ValueError:
                try:
                    self.template.get(version_identifier + "2").value
                    self.is_versioned = True
                    break
                except ValueError:
                    pass

        # If the infobox is not versioned, return False
        if not self.is_versioned:
            self.version_identifiers["id"] = 1
            return False

        # The infobox is versioned... continue processing
        # Try to determine the version counts for each version identifier
        for version_identifier in self.version_identifiers:
            i = 1
            while i <= 50:
                try:
                    self.template.get(version_identifier + str(i)).value
                    self.version_identifiers[version_identifier] += 1
                except ValueError:
                    pass
                i += 1

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

    def extract_infobox_id(self, versioned_identifier: str) -> str:
        """Helper method to extract an ID from a template using harcoded ID keys.

        This helper method is a solution to query an infobox template for
        a unique ID number. The keys used are:
        `id`: Query template using only the string `id`.
        `id + version`: Query template using the string `id` including the `version` number.
        `itemid`: Query template using only the string `itemid`.
        `itemid + version`: Query template using the string `itemid` including the `version` number.

        :param versioned_identifier: The number, as a string, to represent a versioned infobox.
        :return: The extracted template ID value (can be a comma-seperated string).
        """
        value = None
        try:
            value = self.template.get(versioned_identifier).value
            value = value.strip()
            return value
        except ValueError:
            pass

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
        id: 12654 is the airbourne version, that uses version 2 in the infobox
        Returned data: {12647: '1', 12654: '2'}

        Un-versioned example: Pet k'ril tsutsaroth has only one version.
        id: 12652
        Returned data: {12652: ""}
        The empty string indicates that no addition to the `id` property is needed
        to extract the data correctly, as the infobox is not versioned.

        :return: A dictionary mapping item ID to version number.
        """
        item_id_to_version_number = dict()

        # First, try extract the non versioned identifier
        # Example: |id = 10591, followed by |id2 = 10592
        for identifier, count in self.version_identifiers.items():
            # Skip identifiers with no count
            if count == 0:
                continue
            id = self.extract_infobox_id(identifier)  # Pass empty string, not versioned
            if id:
                ids = self.split_infobox_id_string(id)
                for id in ids:
                    id = self.try_int_cast(id)
                    if id is not None:
                        item_id_to_version_number[id] = ""

        if not self.is_versioned:
            return item_id_to_version_number

        # Second, try extract the versioned identifier
        for identifier, count in self.version_identifiers.items():
            # Skip identifiers with no count
            if count == 0:
                continue

            for i in range(1, count + 2):
                id = self.extract_infobox_id(identifier + str(i))  # Pass versioned string
                if id:
                    ids = self.split_infobox_id_string(id)
                    for id in ids:
                        id = self.try_int_cast(id)
                        if id is not None:
                            item_id_to_version_number[id] = i

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
