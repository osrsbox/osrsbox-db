"""
Author:  PH01L
Email:   phoil@osrsbox.com
Website: https://www.osrsbox.com

Description:
Program to invoke item database generation process.

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
import json
import argparse
from pathlib import Path

import config
from builders.items import build_item


class Builder:
    def __init__(self, **kwargs):
        # Set properties to control phases of build
        self.verbose = kwargs["verbose"]
        self.compare = kwargs["compare"]
        self.export = kwargs["export"]
        self.validate = kwargs["validate"]

        # Load the raw cache data that has been processed (this is ground truth)
        with open(Path(config.DATA_ITEMS_PATH / "items-cache-data.json")) as f:
            self.all_items_cache_data = json.load(f)

        # Load all item data (from min JSON file)
        with open(Path(config.DOCS_PATH / "items-complete.json")) as f:
            self.all_db_items = json.load(f)

        # Load the item wikitext file of page text
        with open(Path(config.DATA_ITEMS_PATH / "items-wiki-page-text.json")) as f:
            self.all_wikitext_raw = json.load(f)

        # Load the item wikitext file of processed data
        with open(Path(config.DATA_ITEMS_PATH / "items-wiki-page-text-processed.json")) as f:
            self.all_wikitext_processed = json.load(f)

        # Load dict of unalchable items
        unalchable_items_path = Path(config.DATA_ITEMS_PATH / "items-unalchable.json")
        with open(unalchable_items_path) as f:
            self.unalchable = json.load(f)

        # Load buy limit data
        buy_limits_file_path = Path(config.DATA_ITEMS_PATH / "items-buylimits.json")
        with open(buy_limits_file_path) as f:
            self.buy_limits = json.load(f)

        # Load skill requirement data
        skill_requirements_file_path = Path(config.DATA_ITEMS_PATH / "items-skill-requirements.json")
        with open(skill_requirements_file_path) as f:
            self.skill_requirements = json.load(f)

        # Load stances data
        weapon_stance_file_path = Path(config.DATA_ITEMS_PATH / "weapon-stances.json")
        with open(weapon_stance_file_path) as f:
            self.weapon_stances = json.load(f)

        # Load icon data
        icons_file_path = Path(config.DATA_ICONS_PATH / "icons-items-complete.json")
        with open(icons_file_path) as f:
            self.icons = json.load(f)

        # Load duplicate item data
        duplicates_file_path = Path(config.DATA_ITEMS_PATH / "items-duplicates.json")
        with open(duplicates_file_path) as f:
            self.duplicates = json.load(f)

        # Load schema data
        with open(Path(config.DATA_SCHEMAS_PATH / "schema-items.json")) as f:
            self.schema_data = json.load(f)

        # Initialize a list of known items
        self.known_items = list()

    def run(self):
        # Start processing every item!
        for item_id in self.all_items_cache_data:

            # if int(item_id) < 25800:
            #     continue

            # Skip any beta items
            if "(beta" in self.all_items_cache_data[item_id]["name"]:
                continue

            # Initialize the BuildItem class, used for all items
            builder = build_item.BuildItem(item_id=item_id,
                                           all_items_cache_data=self.all_items_cache_data,
                                           all_db_items=self.all_db_items,
                                           all_wikitext_raw=self.all_wikitext_raw,
                                           all_wikitext_processed=self.all_wikitext_processed,
                                           unalchable=self.unalchable,
                                           buy_limits=self.buy_limits,
                                           skill_requirements=self.skill_requirements,
                                           weapon_stances=self.weapon_stances,
                                           icons=self.icons,
                                           duplicates=self.duplicates,
                                           schema_data=self.schema_data,
                                           known_items=self.known_items,
                                           verbose=self.verbose)

            status = builder.preprocessing()

            if status["status"]:
                builder.populate_wiki_item()
            else:
                builder.populate_non_wiki_item()

            known_item = builder.check_duplicate_item()
            if known_item:
                self.known_items.append(known_item)
            if self.compare:
                builder.compare_new_vs_old_item()
            if self.export:
                builder.export_item_to_json()
            if self.validate:
                builder.validate_item()

        # Done processing, rejoice!
        print("Built.")
        exit(0)

    def test(self):
        # Start processing every item!
        for item_id in self.all_items_cache_data:

            # if int(item_id) < 25800:
            #     continue

            # Skip any beta items
            if "(beta" in self.all_items_cache_data[item_id]["name"]:
                continue

            # Initialize the BuildItem class, used for all items
            builder = build_item.BuildItem(item_id=item_id,
                                           all_items_cache_data=self.all_items_cache_data,
                                           all_db_items=self.all_db_items,
                                           all_wikitext_raw=self.all_wikitext_raw,
                                           all_wikitext_processed=self.all_wikitext_processed,
                                           unalchable=self.unalchable,
                                           buy_limits=self.buy_limits,
                                           skill_requirements=self.skill_requirements,
                                           weapon_stances=self.weapon_stances,
                                           icons=self.icons,
                                           duplicates=self.duplicates,
                                           schema_data=self.schema_data,
                                           known_items=self.known_items,
                                           verbose=self.verbose)

            status = builder.preprocessing()

            if status["status"]:
                builder.populate_wiki_item()
            else:
                builder.populate_non_wiki_item()

            known_item = builder.check_duplicate_item()
            if known_item:
                self.known_items.append(known_item)
            builder.validate_item()

        # Done testing, rejoice!
        print("Tested.")
        exit(0)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Build item database.")
    parser.add_argument('--verbose',
                        default=False,
                        required=False,
                        help='A boolean of whether to be verbose.')
    parser.add_argument('--compare',
                        default=True,
                        required=False,
                        help='A boolean of whether to compare data.')
    parser.add_argument('--export',
                        default=False,
                        required=False,
                        help='A boolean of whether to export data.')
    parser.add_argument('--validate',
                        default=True,
                        required=False,
                        help='A boolean of whether to validate using schema.')
    parser.add_argument('--test',
                        default=False,
                        required=False,
                        help='A boolean of whether to test the builder process.')
    args = parser.parse_args()

    builder = Builder(verbose=args.verbose,
                      compare=args.compare,
                      export=args.export,
                      validate=args.validate)
    if args.test:
        builder.test()
    else:
        builder.run()
