# !/usr/bin/python

"""
Author:  PH01L
Email:   phoil@osrsbox.com
Website: osrsbox.com
Date:    2018/09/15

Description:
Extract all Wikia templates from a list of page titles

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
from collections import defaultdict

def extract_templates(item_name, wikicode_str):
    # page_name = page_name.replace("&", "%26")
    # page_name = page_name.replace("+", "%2B")

    # Parse actual content using mwparser
    wikicode = mwparserfromhell.parse(wikicode_str)
    # Extract templates in the page
    # Three templates of interest:
    # infobox item
    # infobox bonuses
    # infobox construction
    templates = wikicode.filter_templates()
    for template in templates:
        template_name = template.name.strip()
        template_name = template_name.lower()
        if "infobox item" in template_name:
            infobox_items[item_name].append(str(template))
        elif "infobox bonuses" in template_name:
            infobox_bonuses[item_name].append(str(template))
        elif "infobox construction" in template_name:
            infobox_construction[item_name].append(str(template))
        elif "infobox pet" in template_name:
            infobox_pet[item_name].append(str(template))            

################################################################################
if __name__=="__main__":   
    # Start processing
    infobox_items = defaultdict(list)
    infobox_bonuses = defaultdict(list)
    infobox_construction = defaultdict(list)
    infobox_pet = defaultdict(list)
    
    with open("extract_all_items_page_wikitext.txt") as f:
        wikitext_dict = json.load(f)

    for item_name in wikitext_dict:
        print(item_name)
        wikicode_str = wikitext_dict[item_name]
        extract_templates(item_name, wikicode_str)

    print("Total infobox_items: %d" % len(infobox_items))
    print("Total infobox_bonuses: %d" % len(infobox_bonuses))
    print("Total infobox_construction: %d" % len(infobox_construction))
    print("Total infobox_pet: %d" % len(infobox_pet))

    fi_out = "extract_templates_InfoboxItems.txt"
    with open(fi_out, "w") as f:
        json.dump(infobox_items, f)
    fi_out = "extract_templates_InfoboxBonuses.txt"
    with open(fi_out, "w") as f:
        json.dump(infobox_bonuses, f)
    fi_out = "extract_templates_InfoboxConstruction.txt"
    with open(fi_out, "w") as f:
        json.dump(infobox_construction, f)
    fi_out = "extract_templates_InfoboxPet.txt"
    with open(fi_out, "w") as f:
        json.dump(infobox_pet, f)        
