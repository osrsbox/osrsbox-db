"""
Author:  PH01L
Email:   phoil@osrsbox.com
Website: https://www.osrsbox.com

Description:
A very simple example script of how to load the osrsbox-db monster database,
loop through the loaded monsters, and print the monster name to the console.

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

from osrsbox import monsters_api


if __name__ == "__main__":
    # Load all monsters
    all_db_monsters = monsters_api.load()

    item_search_keyword = "prayer potion"

    # Loop through all monsters in the database and search for items by name
    print("The following monsters drop prayer potions!!!")
    print(f"{'ID':<10} {'Name':<25} {'Wiki Name':<25}")
    for monster in all_db_monsters:
        if monster.drops:
            for drop in monster.drops:
                if item_search_keyword in drop.name.lower():
                    print(f"{monster.id:<10} {monster.name:<25} {monster.wiki_name:<25}")
