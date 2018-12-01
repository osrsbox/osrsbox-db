# !/usr/bin/python

"""
Author:  PH01L
Email:   phoil@osrsbox.com
Website: osrsbox.com
Date:    2018/11/30

Description:
Extract all Wikia "Infobox Items" and "Infobox bonuses" 
from a list of page titles. The inputs required are:
extract_all_items.txt from extract_all_items.py
extract_all_other.txt from extract_all_other.txt

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

custom_agent = {
    'User-Agent': 'some-agent',
    'From': 'name@domain.com' 
}

import os
import json
import sys
import requests
import mwparserfromhell
from collections import defaultdict

def extract_InfoboxItem(page_name):
    page_name = page_name.replace("&", "%26")
    page_name = page_name.replace("+", "%2B")
    # Example: http://oldschoolrunescape.wikia.com/api.php?action=parse&prop=wikitext&format=json&page=3rd_age_pickaxe
    url = "https://oldschool.runescape.wiki/api.php?action=parse&prop=wikitext&format=json&page=" + page_name
    result = requests.get(url, headers=custom_agent)
    data = result.json()
    try:
        # Extract the actual content
        input = data["parse"]["wikitext"]["*"].encode("utf-8")
    except KeyError:
        return False
    # Parse actual content using mwparser
    wikicode = mwparserfromhell.parse(input)
    # Dump the entire wikitext to a dict. The dict maps:
    # the item name (page_name) to wikitext object as a string
    all[page_name].append(str(wikicode))

    templates = wikicode.filter_templates()
    for template in templates:
        template_name = template.name.strip()
        template_name = template_name.lower()
        if "bonuses" in template_name:
            bonuses[page_name].append(str(template))
        if "switch infobox" in template_name:
            bonuses[page_name].append(str(template))      

################################################################################
if __name__=="__main__":   
    # Start processing
    all = defaultdict(list)
    bonuses = defaultdict(list)

    # Populate all items (items and other) into a dict
    # Maps item name to None, dict is just for unique strings
    to_process = dict()

    with open("extract_all_items.txt") as f:
        for l in f:
            l = l.strip()
            to_process[l] = None

    with open("extract_all_other.txt") as f:
        for l in f:
            l = l.strip()
            to_process[l] = None

    total = len(to_process)
    count = 0
    for k in to_process:
        sys.stdout.write(">>> Processing: %d or %d, with name: %s\r" % (count, total, k))
        extract_InfoboxItem(k)
        count += 1
    
    # Write all extracted wikitext to a JSON file
    fi_out = "extract_all_items_page_wikitext.txt"
    with open(fi_out, "w") as f:
        json.dump(all, f)

    # Write all extracted wikitext to a JSON file
    fi_out = "extract_all_items_page_wikitext_bonuses.txt"
    with open(fi_out, "w") as f:
        json.dump(bonuses, f)
