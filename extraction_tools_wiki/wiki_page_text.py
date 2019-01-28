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
import requests

LOG = logging.getLogger(__name__)


class WikiPageText:
    """This class handles extraction of wiki text using an OSRS Wiki API query.

    Args:
        page_title (str): OSRS Wiki page titles used for API query.
        out_file_name (str): The file name used for exporting the wiki text to JSON.
        user_agent (str): A custom user-agent name to be used for the API request.
        user_email (str): A custom user-agent email to be used for the API request.

    Attributes:
        base_url (str): The OSRS Wiki URL.
        page_title (str): OSRS Wiki page titles used for API query.
        out_file_name (str): The file name used for exporting the wiki text to JSON.
        custom_agent (dict): A custom user-agent to be used for the API request.
        wiki_text (str): The raw wiki text extracted from the OSRS Wiki.
    """
    def __init__(self, page_title, out_file_name, user_agent, user_email):
        self.base_url = "https://oldschool.runescape.wiki/api.php"
        self.page_title = page_title
        self.out_file_name = out_file_name
        self.custom_agent = {
            'User-Agent': user_agent,
            'From': user_email
        }
        self.wiki_text = None

    def check_revision_date(self, last_revision_date, last_extraction_date):
        """Check the previous revision date to see if the page title needs to be extracted.

        Returns:
            True if the page title is up-to-date, False otherwise.
        """
        return False

    def extract_page_wiki_text(self):
        """Extract wikitext from OSRS Wiki for a provided page name."""
        request = dict()
        request['action'] = 'parse'
        request['prop'] = 'wikitext'
        request['format'] = 'json'
        request['page'] = self.page_title

        page_data = requests.get(self.base_url,
                                 headers=self.custom_agent,
                                 params=request).json()

        try:
            # Try to extract the wikitext from the HTTP response
            wiki_text = page_data["parse"]["wikitext"]["*"].encode("utf-8")
        except KeyError:
            # Set to None if wikitext extraction failed
            wiki_text = None

        self.wiki_text = wiki_text

    def export_wiki_text_to_json(self):
        """Export all extracted wiki text to a JSON file."""
        # Create dictionary for export
        json_data = {self.page_title: str(self.wiki_text)}

        # Write dictionary to JSON file
        if not os.path.isfile(self.out_file_name):
            with open(self.out_file_name, mode='w') as out_file:
                out_file.write(json.dumps(json_data, indent=4))
        else:
            with open(self.out_file_name) as feeds_json:
                feeds = json.load(feeds_json)
            feeds[self.page_title] = str(self.wiki_text)
            with open(self.out_file_name, mode='w') as out_file:
                out_file.write(json.dumps(feeds, indent=4))
