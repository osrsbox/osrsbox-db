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
from pathlib import Path

import config
from items_builder import item_builder


if __name__ == "__main__":
    # Delete old log file
    if os.path.exists("builder.log"):
        os.remove("builder.log")

    # Load the raw output from OSRS cache
    scraper_path = Path(config.DATA_PATH / "items-scraper.json")
    with open(scraper_path) as f:
        cache_items = json.load(f)

    # Load the current database contents
    items_complete_path = Path(config.DOCS_PATH / "items-complete.json")
    with open(items_complete_path) as f:
        current_db = json.load(f)

    # Load the wiki text file
    wiki_text_file_path = Path(config.EXTRACTION_WIKI_PATH / "extract_page_text_items.json")
    with open(wiki_text_file_path) as wiki_text_file:
        wiki_text = json.load(wiki_text_file)

    # Load all normalized names
    normalized_names = dict()
    with open("normalized_names.txt") as f:
        for line in f:
            line = line.strip()
            if "#" in line or line.startswith("TODO"):
                continue
            line = line.split("|")
            normalized_names[line[0]] = [line[1], line[2], line[3]]

    # Load buy limit data
    buy_limits_path = Path(config.DATA_PATH / "ge-limits-names.json")
    with open(buy_limits_path) as f:
        buy_limits = json.load(f)

    # Load skill requirement data
    skill_requirements_path = Path(config.DATA_PATH / "item-skill-requirements.json")
    with open(skill_requirements_path) as f:
        skill_requirements = json.load(f)

    # Start processing every item!
    for item_id in cache_items:
        json_data = cache_items[item_id]

        # Toggle to start, stop at a specific item ID
        # if int(item_id) < 20000:
        #     continue

        # Initialize the BuildItem class
        builder = item_builder.BuildItem(item_id,
                                         json_data,
                                         wiki_text,
                                         normalized_names,
                                         buy_limits,
                                         skill_requirements,
                                         current_db)
        # Start the build item population function
        builder.populate()
    print("Done.")
