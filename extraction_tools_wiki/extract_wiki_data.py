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
import datetime

from .wiki_page_titles import WikiPageTitles
from .wiki_page_text import WikiPageText
from .wiki_text_templates import WikiTextTemplates


if __name__ == "__main__":
    import argparse
    AP = argparse.ArgumentParser()
    AP.add_argument("-c",
                    "--categories",
                    nargs="+",
                    help="<Required> List of OSRS Wiki categories to extract",
                    required=True)
    ARGS = vars(AP.parse_args())

    # List of categories to process from the OSRS Wiki
    TARGET_CATEGORIES = ARGS["categories"]
    PRIMARY_CATEGORY = TARGET_CATEGORIES[0].lower()

    # Specify the custom user agent for all requests
    USER_AGENT = "some-agent"
    USER_EMAIL = "name@domain.com"

    # Boolean to trigger load page titles from file, or run fresh page title extraction
    LOAD_FILES = False

    # Specify the name for the page titles output JSON file
    TITLES_FILE_NAME = "extract_page_titles" + PRIMARY_CATEGORY + ".json"
    TITLES_FILE_PATH = os.path.join("extraction_tools_wiki", TITLES_FILE_NAME)

    # Specify the name for the wiki text output JSON file
    TEXT_FILE_NAME = "extract_page_text" + PRIMARY_CATEGORY + ".json"
    TEXT_FILE_PATH = os.path.join("extraction_tools_wiki", TEXT_FILE_NAME)

    # Set the revision date, extract wiki pages only after this date
    REVISION_DATE = datetime.datetime.strptime("2018-01-01T00:00:00Z",
                                               '%Y-%m-%dT%H:%M:%SZ')

    # Create object to handle page titles extraction
    WIKI_PAGE_TITLES = WikiPageTitles(TARGET_CATEGORIES,
                                      TITLES_FILE_PATH,
                                      USER_AGENT,
                                      USER_EMAIL)

    # Load previously extracted page titles from JSON, or extract from OSRS Wiki API
    if LOAD_FILES:
        WIKI_PAGE_TITLES.load_page_titles()
    else:
        WIKI_PAGE_TITLES.extract_page_titles()
        WIKI_PAGE_TITLES.extract_last_revision_timestamp()
        WIKI_PAGE_TITLES.export_page_titles_in_json()

    print(">>> Number of extracted wiki pages: %d" % len(WIKI_PAGE_TITLES.page_titles))

    print(">>> Starting wiki text extraction for extracted page titles...")
    for page_title, page_revision_date in WIKI_PAGE_TITLES.page_titles.items():
        print("  > Extracting wiki text for: %s" % page_title)
        wiki_page_text = WikiPageText(page_title,
                                      TEXT_FILE_PATH,
                                      USER_AGENT,
                                      USER_EMAIL)
        # If the page title has not been extracted, extract wiki text and save to JSON file
        if not wiki_page_text.has_been_processed():
            wiki_page_text.extract_page_wikitext()
            wiki_page_text.export_wiki_text_to_json()
