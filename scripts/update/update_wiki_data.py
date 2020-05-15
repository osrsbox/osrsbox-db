"""
Author:  PH01L
Email:   phoil@osrsbox.com
Website: https://www.osrsbox.com

Description:
Script to update OSRS Wiki data dump.

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
import argparse

from scripts.wiki import extract_wiki_data


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="Update OSRS Wiki data.")
    parser.add_argument('timestamp',
                        help='A timestamp to start data collection from')
    args = parser.parse_args()

    last_extraction_date = args.timestamp
    print(">>> WIKI DATA ITEMS: Extracting page titles and wiki text...")
    categories = ["Items", "Pets"]
    extract_wiki_data.extract_wiki_data(categories, last_extraction_date)
    print(">>> WIKI DATA MONSTERS: Extracting page titles and wiki text...")
    categories = ["Monsters"]
    extract_wiki_data.extract_wiki_data(categories, last_extraction_date)
    # print(f">>> WIKI DATA QUESTS: Extracting page titles and wiki text...")
    # categories = ["Quests", "Miniquests", "Special_quests"]
    # extract_wiki_data.extract_wiki_data(categories, last_extraction_date)
