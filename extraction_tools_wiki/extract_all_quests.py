# !/usr/bin/python

"""
Author:  PH01L
Email:   phoil@osrsbox.com
Website: osrsbox.com
Date:    2018/01/10

Description:
Extract all quest titles on the OSRS Wiki

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
    1.1.0       Updated script for new OSRS Wiki API
"""

__version__ = "1.1.0"

import requests

custom_agent = {
    'User-Agent': 'some-agent',
    'From': 'name@domain.com'
}


def query_category_items(category):
    for result in query_category_items_callback({'list': 'categorymembers'}, category):
        # Process result data
        for r in result['categorymembers']:
            # print(r["title"])
            fi.write(r["title"])
            fi.write("\n")


def query_category_items_callback(request, category):
    request['action'] = 'query'
    request['format'] = 'json'
    request['cmtitle'] = 'Category:' + category
    request['cmlimit'] = '500'
    lastContinue = {}
    while True:
        # Clone original request
        req = request.copy()
        # Modify the original request
        # Insert values returned in the 'continue' section
        req.update(lastContinue)
        # Call API
        result = requests.get('https://oldschool.runescape.wiki/api.php', headers=custom_agent, params=req).json()
        if 'error' in result:
            print(">>> ERROR!")
            break
        if 'warnings' in result:
            print(result['warnings'])
        if 'query' in result:
            yield result['query']
        if 'continue' not in result:
            break
        lastContinue = result['continue']


################################################################################
if __name__ == "__main__":
    # Start processing
    out_fi = "extract_all_quests.txt"
    fi = open(out_fi, "w")
    query_category_items("Quests")
    query_category_items("Miniquests")
    query_category_items("Special_quests")
    fi.close()
