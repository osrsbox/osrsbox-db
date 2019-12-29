"""
Author:  PH01L
Email:   phoil@osrsbox.com
Website: https://www.osrsbox.com

Description:
Parse raw OSRS Wiki data and produce dict of:
- wiki_page_name
- version_number
- wikitext

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
import json
import logging
import collections
from pathlib import Path

import config
from scripts.wiki.wikitext_parser import WikitextIDParser

logging.basicConfig(filename=Path(__file__).stem+".log",
                    level=logging.DEBUG)
logging.info(">>> Starting process_wikitext.py...")

# Load the wiki text file
wiki_text_file_path = Path(config.DATA_WIKI_PATH / "page-text-items.json")
with open(wiki_text_file_path) as wiki_text_file:
    wiki_text = json.load(wiki_text_file)

# Call WikitextID Parser to map:
# 1. ID to infobox template version
# 2. ID to wikitext entry
template_names = ["infobox item", "infobox pet"]
wiki_data_ids = WikitextIDParser(wiki_text_file_path, template_names)
wiki_data_ids.process_osrswiki_data_dump()

WikiEntry = collections.namedtuple('WikiEntry', 'wiki_page_name version_number wikitext')

export = dict()

for item_id, wikitext in wiki_data_ids.item_id_to_wikitext.items():
    entry = WikiEntry(wiki_page_name=wiki_data_ids.item_id_to_wiki_name[item_id],
                      version_number=wiki_data_ids.item_id_to_version_number[item_id],
                      wikitext=wikitext)
    export[item_id] = entry

out_fi = Path(config.DATA_WIKI_PATH / "processed-wikitext-items.json")
with open(out_fi, 'w') as f:
    json.dump(export, f, indent=4)

logging.info(">>> Starting process_wikitext_monsters.py...")

# Load the wiki text file
wiki_text_file_path = Path(config.DATA_WIKI_PATH / "page-text-monsters.json")
with open(wiki_text_file_path) as wiki_text_file:
    wiki_text = json.load(wiki_text_file)

# Call WikitextID Parser to map:
# 1. ID to infobox template version
# 2. ID to wikitext entry
template_names = ["infobox monster"]
wiki_data_ids = WikitextIDParser(wiki_text_file_path, template_names)
wiki_data_ids.process_osrswiki_data_dump()

WikiEntry = collections.namedtuple('WikiEntry', 'wiki_page_name version_number wikitext')

export = dict()

for item_id, wikitext in wiki_data_ids.item_id_to_wikitext.items():
    entry = WikiEntry(wiki_page_name=wiki_data_ids.item_id_to_wiki_name[item_id],
                      version_number=wiki_data_ids.item_id_to_version_number[item_id],
                      wikitext=wikitext)
    export[item_id] = entry

out_fi = Path(config.DATA_WIKI_PATH / "processed-wikitext-monsters.json")
with open(out_fi, 'w') as f:
    json.dump(export, f, indent=4)
