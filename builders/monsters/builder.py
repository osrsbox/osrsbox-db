"""
Author:  PH01L
Email:   phoil@osrsbox.com
Website: https://www.osrsbox.com

Description:
Program to invoke monster database generation process.

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
from builders.monsters import build_monster


class Builder:
    def __init__(self, **kwargs):
        # Set properties to control phases of build
        self.verbose = kwargs["verbose"]
        self.compare = kwargs["compare"]
        self.export = kwargs["export"]
        self.validate = kwargs["validate"]

        # Load the raw cache data that has been processed (this is ground truth)
        with open(Path(config.DATA_MONSTERS_PATH / "monsters-cache-data.json")) as f:
            self.all_monster_cache_data = json.load(f)

        # Load all monster data (from min JSON file)
        with open(Path(config.DOCS_PATH / "monsters-complete.json")) as f:
            self.all_db_monsters = json.load(f)

        # Load the monster wikitext file of page text
        with open(Path(config.DATA_MONSTERS_PATH / "monsters-wiki-page-text.json")) as f:
            self.all_wikitext_raw = json.load(f)

        # Load the monster wikitext file of processed data
        with open(Path(config.DATA_MONSTERS_PATH / "monsters-wiki-page-text-processed.json")) as f:
            self.all_wikitext_processed = json.load(f)

        # Load the monster processed monster drops
        with open(Path(config.DATA_MONSTERS_PATH / "monsters-drops.json")) as f:
            self.monsters_drops = json.load(f)

        # Load schema data
        with open(Path(config.DATA_SCHEMAS_PATH / "schema-monsters.json")) as f:
            self.schema_data = json.load(f)

        # Initialize a list of known monsters
        self.known_monsters = list()

    def run(self):
        # Start processing every monster!
        for monster_id in self.all_monster_cache_data:

            # if int(monster_id) < 11000:
            #     continue

            # Initialize the BuildMonster class, used for all monsters
            builder = build_monster.BuildMonster(monster_id=monster_id,
                                                 all_monster_cache_data=self.all_monster_cache_data,
                                                 all_db_monsters=self.all_db_monsters,
                                                 all_wikitext_raw=self.all_wikitext_raw,
                                                 all_wikitext_processed=self.all_wikitext_processed,
                                                 monsters_drops=self.monsters_drops,
                                                 schema_data=self.schema_data,
                                                 known_monsters=self.known_monsters,
                                                 verbose=self.verbose)

            status = builder.preprocessing()
            if status:
                builder.populate_monster()
                known_monster = builder.check_duplicate_monster()
                self.known_monsters.append(known_monster)
                builder.populate_monster_drops()
                if self.compare:
                    builder.compare_new_vs_old_monster()
                if self.export:
                    builder.export_monster_to_json()
                if self.validate:
                    builder.validate_monster()

        # Done processing, rejoice!
        print("Built.")
        exit(0)

    def test(self):
        # Start processing every monster!
        for monster_id in self.all_monster_cache_data:

            # if int(monster_id) < 10000:
            #     continue

            # Initialize the BuildMonster class, used for all monsters
            builder = build_monster.BuildMonster(monster_id=monster_id,
                                                 all_monster_cache_data=self.all_monster_cache_data,
                                                 all_db_monsters=self.all_db_monsters,
                                                 all_wikitext_raw=self.all_wikitext_raw,
                                                 all_wikitext_processed=self.all_wikitext_processed,
                                                 monsters_drops=self.monsters_drops,
                                                 schema_data=self.schema_data,
                                                 known_monsters=self.known_monsters,
                                                 verbose=self.verbose)

            status = builder.preprocessing()
            if status:
                builder.populate_monster()
                known_monster = builder.check_duplicate_monster()
                self.known_monsters.append(known_monster)
                builder.populate_monster_drops()
                builder.validate_monster()

        # Done testing, rejoice!
        print("Tested.")
        exit(0)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Build monster database.")
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
