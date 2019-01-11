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
import glob
import requests
import mwparserfromhell
from collections import defaultdict

################################################################################
if __name__=="__main__":   
    # Start processing
    infobox_items = defaultdict(list)
    infobox_bonuses = defaultdict(list)
    infobox_construction = defaultdict(list)
    infobox_pet = defaultdict(list)
    
    # Determine previously extracted wiki pages
    wikitext_fis_path = "extract_all_items_page_wikitext" + os.sep + "*"
    wikitext_fis = glob.glob(wikitext_fis_path)

    to_del = list()
    for fi in wikitext_fis:
        with open(fi) as f:
            data = json.load(f)
            item_name = next(iter(data))
            if "%" in item_name:
                print(item_name)
                to_del.append(fi)        
                
    for fi in to_del:
        os.remove(fi)
            
   
