# !/usr/bin/python

"""
Author:  PH01L
Email:   phoil@osrsbox.com
Website: osrsbox.com
Date:    2018/09/15

Description:
Extract all Wikia "Infobox Items" from a list of page titles

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

import os
import json
import requests
import mwparserfromhell

def extract_InfoboxItem(page_name):
    # Example: http://oldschoolrunescape.wikia.com/api.php?action=parse&prop=wikitext&format=json&page=3rd_age_pickaxe
    url = "http://oldschoolrunescape.wikia.com/api.php?action=parse&prop=wikitext&format=json&page=" + page_name
    result = requests.get(url)
    data = result.json()
    try:
        # Extract the actual content
        input = data["parse"]["wikitext"]["*"].encode("utf-8")
    except KeyError:
        return False
    # Parse actual content using mwparser
    wikicode = mwparserfromhell.parse(input)
    # Extract templates in the page
    templates = wikicode.filter_templates()
    for template in templates:
        template_name = template.name.strip()
        template_name = template_name.lower()
        if "infobox item" in template_name:
            # Save template to: infoboxes_items
            # fi_out = "infoboxes_items" + os.sep + page_name + "--infobox_item"
            # with open(fi_out, "w") as f:
            #     f.write(str(template))
            all[page_name] = str(template)
        elif "infobox construction" in template_name:
            all[page_name] = str(template)

################################################################################
if __name__=="__main__":   
    # Start processing
    all = dict()
    with open("extract_all_construction.txt") as f:
        for l in f:
            l = l.strip()
            print(l)
            extract_InfoboxItem(l)
    fi_out = "extract_infoboxes_construction.txt"
    with open(fi_out, "w") as f:
        json.dump(all, f)
