# !/usr/bin/python

"""
Author:  PH01L
Email:   phoil@osrsbox.com
Website: osrsbox.com
Date:    2018/09/08

Description:
Parse ge_limits.json and add to my existing list.

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
import json

################################################################################
if __name__=="__main__":
    import argparse
    ap = argparse.ArgumentParser()
    ap.add_argument("-r", 
                    "--ge_limits", 
                    required=True,
                    help="RuneLite ge-limits.json file")
    ap.add_argument("-m", 
                    "--extracted_buy_limits", 
                    required=True,
                    help="My extracted_buy_limits.txt file")
    args = vars(ap.parse_args())
    
    # Start processing    
    print(">>> Starting processing...")

    runelite = args["ge_limits"]
    mine = args["extracted_buy_limits"]
    allitems = ".." + os.sep + "docs" + os.sep + "allitems.json"

    print(">>> Processing RuneLite ge-limits.json file: %s" % runelite)
    with open(runelite) as f:
        runelite_dict = json.load(f)

    updated_buy_limits_dict = dict()
    
    print(">>> Processing my extracted_buy_limits.txt file: %s" % mine)
    with open(mine) as f:
        for l in f:
            l = l.strip()
            itemName = l.split("|")[0]
            buyLimit = l.split("|")[1]
            updated_buy_limits_dict[itemName] = buyLimit

    print(">>> Processing allitems.json file: %s" % allitems)
    with open(allitems) as f:
        allitems_dict = json.load(f)
    

    # Find item name from allitems.json
    for itemID, buyLimit in runelite_dict.items():
        itemName = allitems_dict[itemID]["name"]
        if itemName not in updated_buy_limits_dict:
            print("<>><><><><><><><><> FOUND A NEW ONE!")
        updated_buy_limits_dict[itemName] = buyLimit

    # for k,v in updated_buy_limits_dict.items():
    #     print("%s|%s" % (k,v))

