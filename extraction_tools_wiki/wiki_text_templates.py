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
import mwparserfromhell

LOG = logging.getLogger(__name__)


class WikiTextTemplates:
    """This class handles extraction of templates from raw wiki text.

    Args:
        page_title (str): OSRS Wiki page titles used for API query.
        wiki_text (str): The raw wiki text previously extracted from the OSRS Wiki.

    Attributes:
        page_title (str): OSRS Wiki page titles used for API query.
        wiki_text (str): The raw wiki text previously extracted from the OSRS Wiki.
    """
    def __init__(self, page_title, wiki_text):
        self.page_title = page_title
        self.wiki_text = wiki_text

    def extract_templates(self):
        """Extract common OSRS templates from wiki raw text."""
        # List of useful OSRS Wiki templates
        osrs_template_types = ["infobox item",
                               "infobox bonuses",
                               "infobox construction",
                               "infobox pet",
                               "infobox monster"]

        # Parse wiki text using mwparser library
        wiki_text = mwparserfromhell.parse(self.wiki_text)

        # Find any templates in the wiki text
        templates = wiki_text.filter_templates()

        # Loop the templates and search for interesting templates
        for template in templates:
            # Normalize template name
            template_name = template.name.strip()
            template_name = template_name.lower()

            if template_name in osrs_template_types:
                wiki_text_template = str(template)
                wiki_text_template_type = template_name.replace(" ", "_")
                self.export_template(wiki_text_template, wiki_text_template_type)

    def export_template(self, wiki_text_template, wiki_text_template_type):
        """Export any discovered template to corresponding template file.

        Args:
            wiki_text_template (str): An extracted wiki text template.
            wiki_text_template_type (str): The type of OSRS Wiki template.
        """
        # Create dictionary for export
        json_data = {self.page_title: wiki_text_template}

        # Set the output file name
        out_file_name = "extract_page_templates_" + wiki_text_template_type + ".json"
        out_file_path = os.path.join("extraction_tools_wiki", out_file_name)

        # Write dictionary to JSON file
        if not os.path.isfile(out_file_path):
            with open(out_file_path, mode='w') as out_file:
                out_file.write(json.dumps(json_data, indent=4))
        else:
            with open(out_file_path) as feeds_json:
                feeds = json.load(feeds_json)
            feeds[self.page_title] = wiki_text_template
            with open(out_file_path, mode='w') as out_file:
                out_file.write(json.dumps(feeds, indent=4))
