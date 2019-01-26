# !/usr/bin/python

"""
Author:  PH01L
Email:   phoil@osrsbox.com
Website: osrsbox.com
Date:    2019/01/22

Description:
Extract all wikitext from all monster pages. The required input is the
"extract_all_monsters.txt" file from the "extract_all_monsters.py" script.
This script will extract all wikitext to "extract_all_monsters_page_wikitext"
directory for later processing. Monster page wiki text are saved as separate
JSON files with random names.

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
"""

__version__ = "1.0.0"

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
        # Or return if cannot extract wikitext from page
        return

    # Parse actual wikitext content using mwparserfromhell
    wikitext = mwparserfromhell.parse(input)

    # Convert to JSON
    monster_dict = dict()
    monster_dict[page_name] = str(wikitext)

    out_fi_name = ''.join(random.choice(string.ascii_letters + string.digits) for _ in range(64))

    out_fi = os.path.join("extract_all_monsters_page_wikitext", out_fi_name + ".json")
    with open(out_fi, "w") as f:
        json.dump(monster_dict, f)


################################################################################
if __name__ == "__main__":
    # Start processing: extract_all_monsters.txt
    print(">>> Starting to extract wikitext for all monsters...")

    print("  > Reading extract_all_monsters page titles...")
    monsters_to_process = list()
    with open("extract_all_monsters.txt") as f:
        for line in f:
            line = line.strip()
            monsters_to_process.append(line)

    # Determine previously extracted page_titles
    print("  > Determining already extracted page titles...")
    processed_fis_path = os.path.join("extract_all_monsters_page_wikitext", "*")
    processed_fis = glob.glob(processed_fis_path)
    monsters_already_processed = list()
    # Strip path from files
    for fi in processed_fis:
        with open(fi) as f:
            data = json.load(f)
            monster_name = next(iter(data))
            monsters_already_processed.append(monster_name)

    directory = "extract_all_monsters_page_wikitext"
    if not os.path.exists(directory):
        os.makedirs(directory)

    print("  > Starting wikitext extraction...")
    monster_count = len(monsters_to_process)
    count = 0
    for monster_page_title in monsters_to_process:
        sys.stdout.write(">>> Processing: %d out of %d\r" % (count, monster_count))
        if monster_page_title in monsters_already_processed:
            # Skip if already processed
            count += 1
            continue
        # Extract wikitext
        extract_wikitext(monster_page_title)
        count += 1
