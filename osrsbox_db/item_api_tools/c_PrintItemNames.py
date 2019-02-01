# !/usr/bin/python

"""
Author:  PH01L
Email:   phoil@osrsbox.com
Website: osrsbox.com
Date:    2018/12/18

Description:
Simple caller script to print item names

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

from . import AllItems


################################################################################
if __name__ == "__main__":
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
            print(item.id, item.buy_limit)
