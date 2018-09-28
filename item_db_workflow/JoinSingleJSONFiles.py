# !/usr/bin/python

"""
Author:  PH01L
Email:   phoil@osrsbox.com
Website: osrsbox.com
Date:    2018/09/08

Description:
Read the entire docs/items-json directory and create one single 
JSON file.

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
import sys
import json
import glob

###############################################################################
# JoinSingleJSONFiles object
class JoinSingleJSONFiles(object):
    def __init__(self, dir):
        self.dir = dir
        self.allitems_db = dict()

    def process_allitems(self):
        print(">>> Processing dir: %s" % self.dir)
        fis = glob.glob(self.dir + os.sep + "*")
        total = len(fis)
        count = 0
        for fi in fis:
            print(fi)
            with open(fi) as f:
                json_obj = json.load(f)
                # sys.stdout.write(">>> Processing: %d of %d\r" % (count, total))
                self.allitems_db[json_obj["id"]] = json_obj
                count += 1
        # Print length of allitems dict
        with open('allitems_db.json', 'w') as outfile:
            json.dump(self.allitems_db, outfile)

################################################################################
if __name__=="__main__":
    import argparse
    ap = argparse.ArgumentParser()
    ap.add_argument("-d", 
                    "--dir", 
                    required=True,
                    help="Directory of JSON files (docs/items-json/")
    args = vars(ap.parse_args())
    
    # Start processing    
    print(">>> Starting processing...")
    
    j = JoinSingleJSONFiles(args["dir"])
    j.process_allitems()
