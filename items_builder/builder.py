"""
Author:  PH01L
Email:   phoil@osrsbox.com
Website: https://www.osrsbox.com

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
"""

import os
import json

from items_builder import items_build_item


if __name__ == "__main__":
    # Delete old log file
    if os.path.exists(os.path.join("items_build_db", "builder.log")):
        os.remove(os.path.join("items_build_db", "builder.log"))

    # Get the raw output from OSRS cache
    scraper_path = os.path.join("..", "docs", "items-scraper.json")
    with open(scraper_path) as f:
        cache_items = json.load(f)

    # Load the current database contents
    items_complete_path = os.path.join("..", "docs", "items-complete.json")
    with open(items_complete_path) as f:
        current_db = json.load(f)

    # Set data input directories
    extraction_path_wiki = os.path.join("..", "extraction_tools_wiki", "")
    extraction_path_other = os.path.join("..", "extraction_tools_other", "")

    with open(extraction_path_wiki + "extract_page_text_items.json") as wiki_text_file:
        wiki_text = json.load(wiki_text_file)

    # Load all normalized names
    normalized_names = dict()
    with open(extraction_path_other + "normalized_names.txt") as f:
        for line in f:
            line = line.strip()
            if "#" in line or line.startswith("TODO"):
                continue
            line = line.split("|")
            normalized_names[line[0]] = [line[1], line[2], line[3]]

    # Load buy limit data
    buy_limits = dict()
    with open(extraction_path_other + "all_buy_limits.txt") as f:
        for line in f:
            line = line.strip()
            line = line.split("|")
            buy_limits[line[0]] = line[1]

    # Load skill requirement data
    skill_requirements = dict()
    with open(extraction_path_other + "item_skill_requirements.json") as f:
        temp = json.load(f)
        for k, v in temp.items():
            skill_requirements[k] = v

    # Start processing every item!
    for item_id in cache_items:
        json_data = cache_items[item_id]
        # Initialize the BuildItem class
        builder = items_build_item.BuildItem(item_id,
                                             json_data,
                                             wiki_text,
                                             normalized_names,
                                             buy_limits,
                                             skill_requirements,
                                             current_db)
        builder.populate()
