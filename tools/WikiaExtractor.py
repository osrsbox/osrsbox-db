# !/usr/bin/python

"""
Author:  PH01L
Email:   phoil@osrsbox.com
Website: osrsbox.com
Date:    2018/09/04

Description:
WikiaExtractor is a class to extract information about OSRS items from the
OSRS Wikia (oldschoolrunescape.wikia.com) website.

Copyright (c) 2018, PH01L

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

>>> CHANGELOG:
    0.1.0       Base functionality
"""

__version__ = "0.1.0"

# This script will query the OSRS Wikia API
# Technically, it uses the MediaWiki API
# The base URL is: 
# # oldschoolrunescape.wikia.com/api.php?action=<some-type-of-action>

# Summary of API query for Category:Items:
# generator=categorymembers: List of pages that belong to a given category
# gcmtitle=Category:Items: Only get pages in the items category
# prop=categories: Set the properties to categories
# cllimit=max: Specify max number of results to return
# gcmlimit=max: Seems to be same as above, but for gms?
# format=json: Return JSON instead of the XML default

import requests
import json
import wikitextparser

###############################################################################
# WikiaExtractor object
class WikiaExtractor(object):
    def __init__(self):
        self.wikia_item_page_ids = dict()
        self.wikia_buy_limits = dict()

    def query_category_items(self):
        for result in self.query_category_items_callback({'generator': 'categorymembers'}):
            # Process result data
            for r in result['pages']:
                # print(result['pages'][r]['title'])
                page_title = result['pages'][r]['title']
                page_id = result['pages'][r]['pageid']
                self.wikia_item_page_ids[page_title] = page_id

    def query_category_items_callback(self, request):
        request['action'] = 'query'
        request['format'] = 'json'
        request['prop'] = 'categories'
        request['gcmtitle'] = 'Category:Items'
        request['gcmlimit'] = 'max'
        request['cllimit'] = 'max'
        lastContinue = {}
        while True:
            # Clone original request
            req = request.copy()
            # Modify the original request
            # Insert values returned in the 'continue' section
            req.update(lastContinue)
            # Call API
            result = requests.get('http://oldschoolrunescape.wikia.com/api.php', params=req).json()
            if 'error' in result:
                #raise Error(result['error'])
                print(">>> ERROR!")
                break
            if 'warnings' in result:
                print(result['warnings'])
            if 'query' in result:
                yield result['query']
            if 'query-continue' not in result:
                break
            if 'categorymembers' not in result['query-continue']:
                break
            lastContinue = result['query-continue']['categorymembers']

    def parse_buy_limits(self):
        url = "http://oldschoolrunescape.wikia.com/api.php?action=parse&prop=wikitext&format=json&page=Grand_Exchange/Buying_limits"
        result = requests.get(url)
        # Force fetched page to JSON
        data = result.json()
        # Get the actual content (table)
        input = data["parse"]["wikitext"]["*"]
        # Parse the extracted table to WikiText
        p = wikitextparser.parse(input)
        # Grab the first table, there is only one
        t = p.tables[0]
        # Get all the cells as a list
        all_cells = t.cells()
        # Determine number of rows in table
        row_count = len(all_cells)
        #print(row_count)
        for i, cell in enumerate(all_cells):
            item_name = str(all_cells[i][0]) # item_name is in column 1
            if "!Item Name" in item_name:
                continue
            item_name = self.clean_buy_limits(item_name)
            item_buy_limit = str(all_cells[i][1]) # buy_limit is in column 2
            item_buy_limit = self.clean_buy_limits(item_buy_limit)
            self.wikia_buy_limits[item_name] = item_buy_limit

    def clean_buy_limits(self, input):
        # Clean a passed but_limits string
        # For example:
        # item: |[[Zamorak monk top]]
        # buy_limit: |15
        input = input.strip()
        input = input.replace("[", "")
        input = input.replace("]", "")
        input = input.replace("|", "")
        return input  