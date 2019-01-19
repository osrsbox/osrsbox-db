# !/usr/bin/python

"""
Author:  PH01L
Email:   phoil@osrsbox.com
Website: osrsbox.com
Date:    2019/01/19

Description:
Extract all bestiary titles on the OSRS Wiki

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

>>> CHANGELOG:
    1.0.0       Base functionality
    1.1.0       Updated script for new OSRS Wiki API
"""

__version__ = "1.1.0"

import os
import sys
import json
import glob
import random
import string
import requests
import mwparserfromhell

custom_agent = {
    'User-Agent': 'some-agent',
    'From': 'name@domain.com' 
}

def extract_wikitext(page_name):
    url = "https://oldschool.runescape.wiki/api.php?action=parse&prop=wikitext&format=json&page=" + page_name
    result = requests.get(url, headers=custom_agent)
    data = result.json()

    try:
        # Extract the actual content
        input = data["parse"]["wikitext"]["*"].encode("utf-8")
    except KeyError:
        error_fi.write(page_name)
        return

    # Parse actual wikitext content using mwparserfromhell
    wikitext = mwparserfromhell.parse(input)

    # Convert to JSON 
    item_dict = dict()
    item_dict[page_name] = str(wikitext)

    out_fi_name = ''.join(random.choice(string.ascii_letters + string.digits) for _ in range(64))
    
    out_fi = "extract_all_bestiary_page_wikitext" + os.sep + out_fi_name + ".json"
    with open(out_fi, "w") as f:
        json.dump(item_dict, f)

################################################################################
if __name__=="__main__":   
    # Start processing
    bestiary_list = list()
    bestiary_list_file = "extract_all_bestiary_from_defs.txt"
    with open(bestiary_list_file) as f:
        for line in f:
            line = line.strip()
            line = line.split("|")
            beast_id = line[0]
            beast_name = line[1]
            beast_combat_level = line[2]
            bestiary_list.append(beast_name)

    print(">>> Processing %d beasts..." % len(bestiary_list))

    # Determine previously extracted page_titles
    print("  > Determining already extracted page titles...")
    processed_fis_path = "extract_all_bestiary_page_wikitext" + os.sep + "*"
    processed_fis = glob.glob(processed_fis_path)
    titles_already_processed = list()
    # Strip path from files
    for fi in processed_fis:
        with open(fi) as f:
            data = json.load(f)
            item_name = next(iter(data))
            titles_already_processed.append(item_name)

    # Make output directory
    directory = "extract_all_bestiary_page_wikitext"
    if not os.path.exists(directory):
        os.makedirs(directory)    

    # Create output file for missing beasts
    out_fi = "extract_all_bestiary_wikitext_errors.txt"
    error_fi = open(out_fi, "w", newline="\n")

    # Extrack wikitext for page titles
    print("  > Starting wikitext extraction...")
    title_count = len(bestiary_list)
    count = 0
    for page_title in bestiary_list:
        sys.stdout.write(">>> Processing: %d out of %d\r" % (count, title_count))
        if page_title in titles_already_processed:
            # Skip if already processed
            count += 1
            continue
        # Extract wikitext
        extract_wikitext(page_title)
        titles_already_processed.append(page_title)
        count += 1    
