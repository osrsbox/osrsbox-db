# !/usr/bin/python

"""
Author:  PH01L
Email:   phoil@osrsbox.com
Website: osrsbox.com
Date:    2018/09/08

Description:
Extract every InfoboxItem for OSRS Wikia

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

import os
import sys
import json
import requests
import wikitextparser

###############################################################################
# ExtractWikiaItemInfoBoxes object
class ExtractWikiaItemInfoBoxes(object):
    def __init__(self, dir):
        self.dir = dir
        self.allitems_db = dict()

    def process_allitems(self):
        print(">>> Processing dir: %s" % self.dir)
        fis = glob.glob(self.dir + os.sep + "*")
        total = len(fis)
        count = 0
        for fi in fis:
            with open(fi) as f:
                json_obj = json.load(f)
                sys.stdout.write(">>> Processing: %d or %d\r" % (count, total))
                self.allitems_db[json_obj["id"]] = json_obj
                count += 1
        # Print length of allitems dict
        with open('allitems_db.json', 'w') as outfile:
            json.dump(self.allitems_db, outfile)

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


################################################################################
if __name__=="__main__":
    import argparse
    ap = argparse.ArgumentParser()
    ap.add_argument("-d", 
                    "--dir", 
                    required=True,
                    help="Directory of JSON files (docs/items-json/")
    args = vars(ap.parse_args())
    
    # Start processing    
    print(">>> Starting processing...")
    print("  > Comparing old allitems.json to new allitems.json")
    
    j = ExtractWikiaItemInfoBoxes(args["dir"])
    j.process_allitems()
