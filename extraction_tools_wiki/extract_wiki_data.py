"""
Author:  PH01L
Email:   phoil@osrsbox.com
Website: https://www.osrsbox.com

Description:
A Python script to extract all page titles and wiki text from the OSRS Wiki.
The script is capable of extracting data for different categories from the
OSRS Wiki, depending on the command line argument provided by the user.

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
import sys
import json
import datetime
import itertools
from pathlib import Path
from typing import List

import config
from extraction_tools_wiki.wiki_page_titles import WikiPageTitles
from extraction_tools_wiki.wiki_page_text import WikiPageText


OSRS_WIKI_API_URL = "https://oldschool.runescape.wiki/api.php"


def extract_wiki_data(categories: List, last_extraction_date: str):
    """The main function for extracting OSRS Wiki category page titles and page wiki text.

    :param categories: A List containing categories.
    :param last_extraction_date: The date (as a string) of the last extraciton.
    """
    # The first category argument, used to build the output file name
    primary_category = categories[0].lower()

    # Specify the name for the page titles output JSON file
    titles_file_path = f"extract_page_titles_{primary_category}.json"
    titles_file_path = Path(config.EXTRACTION_WIKI_PATH / titles_file_path)

    # Specify the name for the wiki text output JSON file
    text_file_path = f"extract_page_text_{primary_category}.json"
    text_file_path = Path(config.EXTRACTION_WIKI_PATH / text_file_path)

    # STAGE ZERO: SET SCRIPT CONFIGURATION

    # Specify the custom user agent for all requests
    user_agent = "osrsbox-agent"
    user_email = "phoil@osrsbox.com"

    # Boolean to trigger load page titles from file, or run fresh page title extraction
    load_files = False

    # Set the revision date, extract wiki pages only after this date
    last_extraction_date = datetime.datetime.strptime(last_extraction_date,
                                                      '%Y-%m-%dT%H:%M:%SZ')

    # STAGE ONE: EXTRACT PAGE TITLES

    print(">>> Starting wiki page titles extraction...")
    # Create object to handle page titles extraction
    wiki_page_titles = WikiPageTitles(OSRS_WIKI_API_URL,
                                      categories,
                                      user_agent,
                                      user_email)

    # Load previously extracted page titles from JSON, or extract from OSRS Wiki API
    if load_files:
        loaded_page_titles = wiki_page_titles.load_page_titles(titles_file_path)
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
        wiki_page_titles.export_page_titles_in_json(titles_file_path)

    # Determine page titles count
    page_titles_total = len(wiki_page_titles)
    print(f">>> Number of extracted wiki pages: {page_titles_total}")

    # STAGE TWO: EXTRACT WIKI USING PAGE TITLES

    # Open page title JSON file, to check if page needs to have wiki text extracted
    json_data = dict()
    if os.path.isfile(text_file_path):
        with open(text_file_path, mode='r') as existing_out_file:
            json_data = json.load(existing_out_file)

    page_titles_count = 1
    print(">>> Starting wiki text extraction for extracted page titles...")
    for page_title, page_revision_date in wiki_page_titles.page_titles.items():
        print(f"  > Progress: {page_titles_count:4d} of {page_titles_total:4d} - Processing: {page_title}")

        # Convert revision date to datetime object
        last_revision_date = datetime.datetime.strptime(wiki_page_titles[page_title],
                                                        '%Y-%m-%dT%H:%M:%SZ')

        # Check if page title is already present in JSON output file, also check revision date
        if page_title in json_data and last_revision_date < last_extraction_date:
            # If the last revision was before last extract, skip
            page_titles_count += 1
            continue

        # Create object to extract page wiki text
        wiki_page_text = WikiPageText(OSRS_WIKI_API_URL,
                                      page_title,
                                      user_agent,
                                      user_email)

        # If the page title has not been extracted, extract wiki text and save to JSON file
        wiki_page_text.extract_page_wiki_text()
        wiki_page_text.export_wiki_text_to_json(text_file_path)

        page_titles_count += 1


if __name__ == "__main__":
    import argparse
    ap = argparse.ArgumentParser()
    ap.add_argument("-c",
                    "--categories",
                    nargs="+",
                    help="<Required> List of OSRS Wiki categories to extract",
                    required=True)
    args = vars(ap.parse_args())

    # List of categories to process from the OSRS Wiki
    target_categories = args["categories"]
    extract_wiki_data(target_categories, "2019-06-14T00:00:00Z")
