# !/usr/bin/python

"""
Author:  PH01L
Email:   phoil@osrsbox.com
Website: osrsbox.com
Date:    2019/01/22

Description:


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
import json

# These require pip install
import mwparserfromhell

extraction_path_wiki = ".." + os.sep + "extraction_tools_wiki" + os.sep

with open(extraction_path_wiki + "extract_all_monsters_page_wikitext.json") as f:
    all_wiki_monsters = json.load(f)

for name in all_wiki_monsters:
    # print(name)
    wikitext = mwparserfromhell.parse(all_wiki_monsters[name])

    # Extract Infobox Monster template in the page
    found_template = False
    monster_template = None
    templates = wikitext.filter_templates()
    for template in templates:
        template_name = template.name.strip()
        template_name = template_name.lower()
        if "infobox monster" in template_name:
            found_template = True
            monster_template = template

    # is_versioned = has multiple versions available
    # version_count = the number of versions available
    is_versioned = False
    version_count = 0
    if found_template:
        # Check if the infobox is versioned
        try:
            monster_template.get("version1").value
            is_versioned = True
            # Now, try to determine how many versions are present
            i = 1
            while i <= 20: # Guessing max verison number, using 20
                version_number = "version" + str(i) # e.g., version1, version2
                try:
                    monster_template.get(version_number).value
                    version_count += 1
                except ValueError:
                    break
                i += 1
        except ValueError:
            pass

        if is_versioned:
            print(">>> Name      %s" % name)
            print("  > Versions: %d" % version_count)
        else:
            print(">>> Name      %s" % name)
            print("  > Versions: %d" % 1)
                