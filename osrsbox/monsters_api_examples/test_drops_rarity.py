"""
Author:  PH01L
Email:   phoil@osrsbox.com
Website: https://www.osrsbox.com

Description:
A simple script to calculate the rarity of monster drops.

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

from osrsbox import monsters_api


if __name__ == "__main__":
    # Load all monsters
    all_db_monsters = monsters_api.load()

    # Loop through all monsters in the database and search for items by name
    print(f"{'ID':<10} {'Name':<25} {'Rarity Total':<25}")
    for monster in all_db_monsters:
        if monster.drops:
            total_drop_rarity = 0
            for drop in monster.drops:
                if drop.rarity == 1.0:
                    continue
                total_drop_rarity += drop.rarity
            print(f"{monster.id:<10} {monster.name:<25} {total_drop_rarity:<25}")
