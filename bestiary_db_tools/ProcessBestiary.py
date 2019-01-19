# !/usr/bin/python

"""
Author:  PH01L
Email:   phoil@osrsbox.com
Website: osrsbox.com
Date:    2019/01/19

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
    0.1.0       Base functionality
"""

__version__ = "0.1.0"

import os
import sys
import json
import glob

sys.path.append(os.getcwd())
import BeastDefinition

###############################################################################
# ProcessBestiary object
class ProcessBestiary(object):
    def __init__(self, all_bestiary_names, all_wiki_bestiary, wiki_extraction_errors):
        self.all_bestiary_names = all_bestiary_names
        self.all_wiki_bestiary = all_wiki_bestiary
        self.wiki_extraction_errors = wiki_extraction_errors      

    def process_all_beasts(self):
        # Loop through every item
        print(">>> Processing all beasts...")
        # Print length
        print("  > Total beast count: %d" % len(self.all_bestiary_names))
        # Individually process each item
        for beast_data in all_bestiary_names:
            self.construct_BeastDefinition(beast_data)

    def construct_BeastDefinition(self, beast_data):
        beast_def = BeastDefinition.BeastDefinition(beast_data, self.all_wiki_bestiary, self.wiki_extraction_errors) 
        beast = beast_def.populate()

################################################################################
if __name__=="__main__":    
    # Start processing    
    print(">>> Starting processing...")

    # Remove old log file
    if os.path.exists("BeastDefinition.log"):
        os.remove("BeastDefinition.log")

    extraction_path_wiki = ".." + os.sep + "extraction_tools_wiki" + os.sep
    extraction_path_other = ".." + os.sep + "extraction_tools_other" + os.sep

    with open(extraction_path_wiki + "extract_all_bestiary_page_wikitext.json") as f:
        all_wiki_bestiary = json.load(f)

    wiki_extraction_errors = list()
    with open(extraction_path_wiki + "extract_all_bestiary_wikitext_errors.txt") as f:
        for line in f:
            line = line.strip()
            wiki_extraction_errors.append(line)

    all_bestiary_names = list()
    with open(extraction_path_wiki + "extract_all_bestiary_from_defs.txt") as f:
        for line in f:
            line = line.strip()
            all_bestiary_names.append(line)

    # Next, build the ProcessItems class to handle all items
    pb = ProcessBestiary(all_bestiary_names,
                         all_wiki_bestiary,
                         wiki_extraction_errors)
    
    # Check for already processes files in items-json (in this dir)
    # pi.determine_already_processed()

    # Start processing each item ID
    pb.process_all_beasts()
