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

    :param str page_title: OSRS Wiki page titles used for API query.
    :param str out_file_name: The file name used for exporting the wiki text to JSON.
    :param str user_agent: A custom user-agent name to be used for the API request.
    :param str user_email: A custom user-agent email to be used for the API request.
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

    def extract_page_wiki_text(self):
        """Extract wikitext from OSRS Wiki for a provided page name.

        This function uses the class attributes as input to query the OSRS Wiki
        API and extract the wiki text for a specific page. The page to query is
        determined by the page title.
        """
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
        """Export all extracted wiki text to a JSON file.

        Querying the OSRS Wiki constantly is a bad approach. This function writes any
        extracted wiki text to a file to save re-querying the API. This function
        attempts to overwrite pre-existing wiki text entry in a file, where the key
        is the page title, and the value is the wiki text.
        """
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
