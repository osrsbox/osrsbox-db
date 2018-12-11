# !/usr/bin/python

"""
Author:  PH01L
Email:   phoil@osrsbox.com
Website: osrsbox.com
Date:    2018/09/01

Description:
Simple caller script

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
import sys
sys.path.append(os.getcwd())
import AllItems
import ItemDefinition
import ItemBonuses

################################################################################
if __name__=="__main__":
    import argparse
    ap = argparse.ArgumentParser()
    ap.add_argument("-i", 
                    "--input", 
                    required=True,
                    help="Two options: 1) Directory of JSON item files (../docs/items-json), or 2) Single JSON file (../docs/items_complete.json) ")
    args = vars(ap.parse_args())
    
    # Start processing    
    print(">>> Starting processing AllItems...")
    ai = AllItems.AllItems(args["input"])
    print(">>> Finished processing AllItems...")

    for item in ai:
        if item.name is not None:
            print(item.id, item.name)

    # # Count equipable items:
    # total_count = 0
    # equipable_count = 0
    # for item in ai:
    #     if item.equipable:
    #         equipable_count += 1
    #     total_count += 1 
    # print(">>> In OSRS there are %d equipable items out of %d total items!" % (equipable_count, total_count))

    # Management/Processing code commented below:

    # # Make an output directory for any modified JSON files
    # directory = "items-json"
    # if not os.path.exists(directory):
    #     os.makedirs(directory)

    # # Temp code to fix old Wikia URLs
    # for item in ai:
    #     print("Processing: %s" % item.id)
    #     if item.url == None:
    #         continue
    #     elif item.url == "":
    #         item.url = None
    #         item.export_pretty_json()
    #     elif item.url == "http://oldschoolrunescape.wikia.com/wiki/":
    #         item.url = None
    #         item.export_pretty_json()
    #     elif "http://oldschoolrunescape.wikia.com/wiki/" in item.url:
    #         item.url = item.url.replace("http://oldschoolrunescape.wikia.com/wiki/", "https://oldschool.runescape.wiki/w/")
    #         item.export_pretty_json()
    #     elif "https://oldschoolrunescape.wikia.com/wiki/" in item.url:
    #         item.url = item.url.replace("https://oldschoolrunescape.wikia.com/wiki/", "https://oldschool.runescape.wiki/w/")
    #         item.export_pretty_json()

    # # Simple diff for before and after
    # import glob

    # moded_fis = [os.path.basename(x) for x in glob.glob("items-json/*")]
    # existing_fis = [os.path.basename(x) for x in glob.glob("../docs/items-json/*")]
    # print(len(moded_fis))
    # print(len(existing_fis))
    # diff = list(set(existing_fis) - set(moded_fis))
    # print(diff)
