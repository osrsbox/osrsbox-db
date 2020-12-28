"""
Author:  PH01L
Email:   phoil@osrsbox.com
Website: https://www.osrsbox.com

Description:
Script to update OSRS cache data dump.

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
from scripts.cache import generate_items_stacked_variants
from scripts.cache import generate_items_cache_data
from scripts.cache import generate_monsters_cache_data
from scripts.cache import generate_summary_files
from scripts.cache import generate_summary_models
from scripts.cache import determine_changes


def main():
    print(">>> generate_items_stacked_variants...")
    generate_items_stacked_variants.process()

    print(">>> generate_items_cache_data...")
    generate_items_cache_data.process()

    print(">>> generate_monsters_cache_data...")
    generate_monsters_cache_data.process()

    print(">>> generate_summary_files...")
    generate_summary_files.process()

    print(">>> generate_summary_models...")
    generate_summary_models.process()

    print(">>> determine_changes...")
    determine_changes.items()
    determine_changes.monsters()
    determine_changes.move()


if __name__ == '__main__':
    main()
