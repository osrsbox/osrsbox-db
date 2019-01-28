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
import itertools
import requests

LOG = logging.getLogger(__name__)


class WikiPageTitles:
    """This class handles extraction of wiki page titles by category using an OSRS Wiki API query.

    Args:
        categories (:obj:`list` of :obj:`str`): A list of OSRS Wiki categories.
        out_file_name (str): The file name used for exporting the wiki page titles to JSON.
        user_agent (str): A custom user-agent name to be used for the API request.
        user_email (str): A custom user-agent email to be used for the API request.

    Attributes:
        base_url (str): The OSRS Wiki URL.
        categories (:obj:`list` of :obj:`str`): A list of OSRS Wiki categories.
        out_file_name (str): The file name used for exporting the wiki text to JSON.
        custom_agent (dict): A custom user-agent to be used for the API request.
    """
    def __init__(self, categories, out_file_name, user_agent, user_email):
        self.base_url = "https://oldschool.runescape.wiki/api.php"
        self.page_titles = dict()
        self.categories = categories
        self.out_file_name = out_file_name
        self.custom_agent = {
            'User-Agent': user_agent,
            'From': user_email
        }

    def __iter__(self):
        for page_title in self.page_titles:
            yield page_title

    def load_page_titles(self):
        """Load a JSON file of OSRS Wiki page titles that have previously been extracted."""
        with open(self.out_file_name) as input_json_file:
            self.page_titles = json.load(input_json_file)

    def extract_page_titles(self):
        """Query a list of categories in the OSRS Wiki and return a list of page titles."""
        for category in self.categories:
            self.extract_page_titles_from_category(category)

    def extract_page_titles_from_category(self, category):
        """Query a specific category in the OSRS Wiki and populate a list of page tiles."""
        # Construct MediaWiki request
        request = {'list': 'categorymembers'}

        for result in self.extract_page_titles_from_category_callback(request, category):
            # Process JSON result data
            for entry in result['categorymembers']:
                page_title = entry["title"]
                if page_title.startswith("File:"):
                    continue

                # Log the page title, and append to list
                self.page_titles[page_title] = None

    def extract_page_titles_from_category_callback(self, request, category):
        """Query callback function for OSRS Wiki category query."""
        request['cmtitle'] = 'Category:' + category
        request['action'] = 'query'
        request['format'] = 'json'
        request['cmlimit'] = '500'
        last_continue = dict()

        while True:
            # Clone original request
            req = request.copy()

            # Insert the 'continue' section to the request
            req.update(last_continue)

            # Perform HTTP GET request
            result = requests.get(self.base_url,
                                  headers=self.custom_agent,
                                  params=req).json()

            # Handle HTTP response
            if 'query' in result:
                # If "query" entry is in JSON result, extract the query response
                yield result['query']
            if 'continue' not in result:
                # If "continue" entry is not JSON result, there are no more page titles in category
                break
            if 'errors' in result:
                print(result['errors'])
                break
            if 'warnings' in result:
                print(result['warnings'])
                break

            # Update the page to continue query
            last_continue = result['continue']

    def extract_last_revision_timestamp(self):
        """Extract the last revision timestamp for all page titles from OSRS Wiki."""
        # Loop 50 page titles at a time, the max number for a revisions request using page titles
        for block_list in itertools.zip_longest(*[iter(self.page_titles)] * 50):
            # Remove None entries from the list of page titles
            block_list = filter(None, block_list)

            # Join page titles for API query in required format
            page_titles_string = "|".join(block_list)

            # Construct query for fetching page revisions
            request = dict()
            request['action'] = 'query'
            request['prop'] = 'revisions'
            request['titles'] = page_titles_string
            request['format'] = 'json'
            request['rvprop'] = 'timestamp'

            page_data = requests.get(self.base_url,
                                     headers=self.custom_agent,
                                     params=request).json()

            # Loop returned page revision data
            pages = page_data["query"]["pages"]
            for page_id in pages:
                # Extract page title from the response
                page_title = pages[page_id]["title"]
                # Extract last revision timestamp (ISO 8601 format)
                page_revision_date = pages[page_id]["revisions"][0]["timestamp"]
                # Add revision date to page_titles dict
                self.page_titles[page_title] = page_revision_date

    def export_page_titles_in_json(self):
        """Export all extracted page titles and revision timestamp to a JSON file."""
        with open(self.out_file_name, mode='w') as out_file:
            out_file.write(json.dumps(self.page_titles, indent=4))

    def export_page_titles_in_text(self):
        """Export all extracted page titles from a category to a text file."""
        with open(self.out_file_name, mode='w', newline='\n') as out_file:
            for page_title in self.page_titles:
                out_file.write(page_title + '\n')
