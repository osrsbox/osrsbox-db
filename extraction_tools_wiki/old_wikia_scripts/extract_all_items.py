# !/usr/bin/python

"""
Author:  PH01L
Email:   phoil@osrsbox.com
Website: osrsbox.com
Date:    2018/09/01

Description:
Extract all items on the OSRS Wiki

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
    1.0.0       Base functionality
"""

__version__ = "1.0.0"

import requests


def query_category_items():
    for result in query_category_items_callback({'generator': 'categorymembers'}):
        # Process result data
        for r in result['pages']:
            print(result['pages'][r]["title"])


def query_category_items_callback(request):
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
        # print(result)
        if 'error' in result:
            # raise Error(result['error'])
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


################################################################################
if __name__ == "__main__":
    # Start processing
    query_category_items()
