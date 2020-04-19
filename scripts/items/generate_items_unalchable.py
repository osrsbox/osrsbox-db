"""
Author:  PH01L
Email:   phoil@osrsbox.com
Website: https://www.osrsbox.com

Description:
Fetch a list of unalchable items from the OSRS Wiki.

Copyright (c) 2020, PH01L

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
from pathlib import Path

import config
from scripts.wiki.wiki_page_titles import WikiPageTitles

OSRS_WIKI_API_URL = "https://oldschool.runescape.wiki/api.php"


def main():
    # The first category argument, used to build the output file name
    primary_category = "unalchable"
    categories = ["Items_that_cannot_be_alchemised"]

    # Specify the name for the page titles output JSON file
    titles_file_path = f"page-titles-{primary_category}.json"
    titles_file_path = Path(config.DATA_WIKI_PATH / titles_file_path)

    # Specify the custom user agent for all requests
    user_agent = "osrsbox-agent"
    user_email = "phoil@osrsbox.com"

    print(">>> Starting wiki page titles extraction...")
    # Create object to handle page titles extraction
    wiki_page_titles = WikiPageTitles(OSRS_WIKI_API_URL,
                                      categories,
                                      user_agent,
                                      user_email)

    wiki_page_titles.extract_page_titles()
    wiki_page_titles.export_page_titles_in_json(titles_file_path)

    # Determine page titles count
    page_titles_total = len(wiki_page_titles)
    print(f">>> Number of extracted wiki pages: {page_titles_total}")


if __name__ == "__main__":
    main()
