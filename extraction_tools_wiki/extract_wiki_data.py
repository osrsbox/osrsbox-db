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

from extraction_tools_wiki.wiki_page_titles import WikiPageTitles
from extraction_tools_wiki.wiki_page_text import WikiPageText


OSRS_WIKI_API_URL = "https://oldschool.runescape.wiki/api.php"

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
    # The first category argument, used to build the output file name
    primary_category = target_categories[0].lower()

    # Specify the name for the page titles output JSON file
    titles_file_name = f"extract_page_titles_{primary_category}.json"
    titles_file_path = os.path.join("extraction_tools_wiki", titles_file_name)

    # Specify the name for the wiki text output JSON file
    text_file_name = f"extract_page_text_{primary_category}.json"
    text_file_path = os.path.join("extraction_tools_wiki", text_file_name)

    # STAGE ZERO: SET SCRIPT CONFIGURATION

    # Specify the custom user agent for all requests
    user_agent = "some-agent"
    user_email = "name@domain.com"

    # Boolean to trigger load page titles from file, or run fresh page title extraction
    load_files = True

    # Set the revision date, extract wiki pages only after this date
    last_extraction_date = datetime.datetime.strptime("2019-01-28T00:00:00Z",
                                                      '%Y-%m-%dT%H:%M:%SZ')

    # STAGE ONE: EXTRACT PAGE TITLES

    print(">>> Starting wiki page titles extraction...")
    # Create object to handle page titles extraction
    wiki_page_titles = WikiPageTitles(OSRS_WIKI_API_URL,
                                      target_categories,
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
    print(">>> Number of extracted wiki pages: %d" % page_titles_total)

    # STAGE TWO: EXTRACT WIKI USING PAGE TITLES

    # Open page title JSON file, to check if page needs to have wiki text extracted
    json_data = dict()
    if os.path.isfile(text_file_path):
        with open(text_file_path, mode='r') as existing_out_file:
            json_data = json.load(existing_out_file)

    page_titles_count = 1
    print(">>> Starting wiki text extraction for extracted page titles...")
    for page_title, page_revision_date in wiki_page_titles.page_titles.items():
        print("  > Progress: %s of %s - Processing: %s" % ('{:4d}'.format(page_titles_count),
                                                           '{:4d}'.format(page_titles_total),
                                                           page_title))

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
