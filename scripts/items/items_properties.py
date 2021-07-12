"""
Author:  PH01L
Email:   phoil@osrsbox.com
Website: https://www.osrsbox.com

Description:
Script to fetch OSRS Wiki pages for Category:Items.

Copyright (c) 2021, PH01L

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
import sys
import json
import itertools
import collections
from pathlib import Path
from datetime import datetime
from datetime import timedelta

import config
from scripts.wiki.wiki_page_titles import WikiPageTitles
from scripts.wiki.wiki_page_text import WikiPageText
from scripts.wiki.wikitext_parser import WikitextIDParser


OSRS_WIKI_API_URL = "https://oldschool.runescape.wiki/api.php"
TITLES_FP = Path(config.DATA_ITEMS_PATH / "items-wiki-page-titles.json")
TEXT_FP = Path(config.DATA_ITEMS_PATH / "items-wiki-page-text.json")


def fetch():
    """Get all the wiki category page titles and page text."""
    # Try to determine the last update
    if TITLES_FP.exists():
        stream = os.popen(f"git log -1 --format='%ad' {TITLES_FP}")
        last_extraction_date = stream.read()
        last_extraction_date = last_extraction_date.strip()
        last_extraction_date = last_extraction_date.replace(" +1200", "")
        last_extraction_date = datetime.strptime(last_extraction_date, "%a %b %d %H:%M:%S %Y")
        last_extraction_date = last_extraction_date - timedelta(days=3)
    else:
        last_extraction_date = datetime.strptime("2013-02-22", "%Y-%m-%d")

    print(">>> Starting wiki page titles extraction...")
    # Create object to handle page titles extraction
    wiki_page_titles = WikiPageTitles(OSRS_WIKI_API_URL,
                                      ["Items", "Pets"])

    # Boolean to trigger load page titles from file, or run fresh page title extraction
    load_files = False

    # Load previously extracted page titles from JSON, or extract from OSRS Wiki API
    if load_files:
        loaded_page_titles = wiki_page_titles.load_page_titles(TITLES_FP)
        if not loaded_page_titles:
            sys.exit(">>> ERROR: Specified page titles to load, but not file found. Exiting.")
    else:
        # Extract page titles using supplied categories
        wiki_page_titles.extract_page_titles()
        # Extract page revision date
        # Loop 50 page titles at a time, the max number for a revisions request using page titles
        for page_title_list in itertools.zip_longest(*[iter(wiki_page_titles.page_titles)] * 50):
            # Remove None entries from the list of page titles
            page_title_list = filter(None, page_title_list)
            # Join the page titles list using the pipe (|) separator
            page_titles_string = "|".join(page_title_list)
            # Extract the page revision date
            wiki_page_titles.extract_last_revision_timestamp(page_titles_string)
        # Save all page titles and
        wiki_page_titles.export_page_titles_in_json(TITLES_FP)

    # Determine page titles count
    page_titles_total = len(wiki_page_titles)
    print(f">>> Number of extracted wiki pages: {page_titles_total}")

    # Open page title JSON file, to check if page needs to have wiki text extracted
    json_data = dict()

    if TEXT_FP.exists():
        with open(TEXT_FP, mode="r") as existing_out_file:
            json_data = json.load(existing_out_file)

    page_titles_count = 1
    print(">>> Starting wiki text extraction for extracted page titles...")
    for page_title, page_revision_date in wiki_page_titles.page_titles.items():
        print(f"  > Progress: {page_titles_count:4d} of {page_titles_total:4d} - Processing: {page_title}")

        # If script fails:
        # 1) Set load_files (above) to True
        # 2) Uncomment code below, and set item ID to last failed item
        # 3) Use this script: python monster_properties_fetch -c Items, Pets
        # if int(page_titles_count) < 5400:
        #     page_titles_count += 1
        #     continue

        # Convert revision date to datetime object
        last_revision_date = datetime.strptime(wiki_page_titles[page_title],
                                               "%Y-%m-%dT%H:%M:%SZ")

        # Check if page title is already present in JSON output file, also check revision date
        if page_title in json_data and last_revision_date < last_extraction_date:
            # If the last revision was before last extract, skip
            page_titles_count += 1
            continue

        # Create object to extract page wiki text
        wiki_page_text = WikiPageText(OSRS_WIKI_API_URL,
                                      page_title)

        # If the page title has not been extracted, extract wiki text and save to JSON file
        wiki_page_text.extract_page_wiki_text()
        wiki_page_text.export_wiki_text_to_json(TEXT_FP)

        page_titles_count += 1


def process():
    print(">>> Starting wiki page text processing...")

    # Call WikitextIDParser to map:
    # 1. ID to infobox template version
    # 2. ID to wikitext entry
    template_names = ["infobox item", "infobox pet"]
    wiki_data_ids = WikitextIDParser(TEXT_FP, template_names)
    wiki_data_ids.process_osrswiki_data_dump()

    WikiEntry = collections.namedtuple('WikiEntry', 'wiki_page_name version_number wikitext')

    export = dict()

    for item_id, wikitext in wiki_data_ids.item_id_to_wikitext.items():
        entry = WikiEntry(wiki_page_name=wiki_data_ids.item_id_to_wiki_name[item_id],
                          version_number=wiki_data_ids.item_id_to_version_number[item_id],
                          wikitext=wikitext)
        export[item_id] = entry

    out_fi = Path(config.DATA_ITEMS_PATH / "items-wiki-page-text-processed.json")
    with open(out_fi, 'w') as f:
        json.dump(export, f, indent=4)


if __name__ == "__main__":
    fetch()
    process()
