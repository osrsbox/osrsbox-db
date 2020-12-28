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
from typing import Dict
from typing import Generator

import requests

import config

LOG = logging.getLogger(__name__)


class WikiPageTitles:
    """This class handles extraction of wiki page titles by category using an OSRS Wiki API query.

    :param base_url: The OSRS Wiki URL used for API queries.
    :param categories: A list of OSRS Wiki categories.
    """
    def __init__(self, base_url: str, categories: list):
        self.base_url = base_url
        self.categories = categories
        self.page_titles: Dict[str, str] = dict()

    def __iter__(self) -> Generator[str, None, None]:
        """Iterate (loop) over the extracted or loaded OSRS Wiki page titles.

        :return: An extracted page title from the OSRS Wiki for a specific category.
        """
        for page_title in self.page_titles:
            yield page_title

    def __len__(self) -> int:
        """Return the length of the extract or loaded OSRS Wiki page titles.

        :return: The number of extracted or loaded page titles.
        """
        return len(self.page_titles)

    def __getitem__(self, key: str) -> str:
        """Return the revision date of the provided page title.

        :param key: The page title to extract the revision date from.
        :return last_revision_date: The date the page was last modified in a string ISO8601 format.
        :rtype str:
        """
        return self.page_titles[key]

    def load_page_titles(self, in_file_name: str) -> bool:
        """Load a JSON file of OSRS Wiki page titles that have previously been extracted.

        If you already have a recently dumped JSON file of OSRS Wiki page titles you
        can load them using this function. This saves performing additional wiki API
        queries when you have an up-to-date list of page titles.

        :param in_file_name: The name of the file to load page titles from.
        :return: A boolean to indicate if a file with page titles was loaded correctly.
        """
        if not Path.exists(in_file_name):
            return False
        with open(in_file_name) as input_json_file:
            self.page_titles = json.load(input_json_file)
            return True

    def extract_page_titles(self):
        """Query a list of categories in the OSRS Wiki and return a list of page titles.

        This function is used to loop the list of categories that you want to extract
        from the OSRS Wiki using the MediaWiki API. You can all it using one category,
        for example: `Items`. Or you can use a list of category strings, for example:
        `Items, Pets, Furniture`.
        """
        for category in self.categories:
            self.extract_page_titles_from_category(category)

    def extract_page_titles_from_category(self, category: str):
        """Query a specific category in the OSRS Wiki and populate a list of page tiles.

        A function to extract all page titles from a provided OSRS Wiki category. The
        extracted page title is useful to perform additional API queries, such as
        extracting wiki text or revision timestamps.

        :param category: A string representing the OSRS Wiki category to extract.
        """
        # Start construct MediaWiki request
        request = {'list': 'categorymembers'}

        for result in self._extract_page_titles_from_category_callback(request, category):
            # Process JSON result data
            for entry in result['categorymembers']:
                page_title = entry["title"]
                if page_title.startswith("File:"):
                    continue
                if page_title.startswith("Category:"):
                    continue

                # Log the page title, and append to list
                self.page_titles[page_title] = None

    def _extract_page_titles_from_category_callback(self, request: Dict, category: str):
        """Query callback function for OSRS Wiki category query.

        A callback function for using MediaWiki generators. Since the category query is a
        list function, you can use a generator to continue queries when the returned data
        is longer than the maximum returned query.

        :param request: A dictionary to be populated with the OSRS Wiki API request.
        :param category: A string representing the OSRS Wiki category to extract.
        """
        request['cmtitle'] = f'Category:{category}'
        request['action'] = 'query'
        request['format'] = 'json'
        request['cmlimit'] = '500'

        last_continue = {}

        while True:
            # Clone original request
            req = request.copy()

            # Insert the 'continue' section to the request
            req.update(last_continue)

            # Perform HTTP GET request
            try:
                result = requests.get(self.base_url,
                                      headers=config.custom_agent,
                                      params=req).json()
            except requests.exceptions.RequestException as e:
                raise SystemExit(">>> ERROR: Get request error. Exiting.") from e

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

            # Update the last fetched page title to continue query
            last_continue = result['continue']

    def extract_last_revision_timestamp(self, page_titles_string: str) -> Dict:
        """Extract the last revision timestamp for page titles from OSRS Wiki.

        The MediaWiki API used by the OSRS Wiki has the functionality to return the
        last revision date of a specific page. This function extracts the revision
        date for a list of extracted page titles. This value can be used to determine
        if changes have recently been made to the page, and if the page should be
        processed again. The input page_titles_string needs to be a list of page
        titles separated by the pipe (|) character. The maximum number of page titles
        is 50 per API query.

        :param page_titles_string: A string of pipe separated wiki page titles.
        :return pages_revision_data:
        """
        # Construct query for fetching page revisions
        request = {
            'action': 'query',
            'prop': 'revisions',
            'titles': page_titles_string,
            'format': 'json',
            'rvprop': 'timestamp'
        }

        page_data = requests.get(self.base_url,
                                 headers=config.custom_agent,
                                 params=request).json()

        # Loop returned page revision data
        pages_revision_data = page_data["query"]["pages"]
        for page_id in pages_revision_data:
            # Extract page title from the response
            page_title = pages_revision_data[page_id]["title"]
            # Extract last revision timestamp (ISO 8601 format)
            page_revision_date = pages_revision_data[page_id]["revisions"][0]["timestamp"]
            # Add revision date to page_titles dict
            self.page_titles[page_title] = page_revision_date

        return pages_revision_data

    def export_page_titles_in_json(self, out_file_name: str):
        """Export all extracted page titles and revision timestamp to a JSON file.

        :param out_file_name: The file name used for exporting the wiki page titles to JSON.
        """
        with open(out_file_name, mode='w') as out_file:
            out_file.write(json.dumps(self.page_titles, indent=4))

    def export_page_titles_in_text(self, out_file_name: str):
        """Export all extracted page titles from a category to a text file.

        :param out_file_name: The file name used for exporting the wiki page titles to a text file.
        """
        with open(out_file_name, mode='w', newline='\n') as out_file:
            for page_title in self.page_titles:
                out_file.write(page_title + '\n')
