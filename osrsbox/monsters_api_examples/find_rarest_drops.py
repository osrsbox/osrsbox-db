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

from collections import defaultdict

from osrsbox import monsters_api


if __name__ == "__main__":
    # Load all monsters
    all_db_monsters = monsters_api.load()

    rarest_drop = defaultdict(list)
    rarest_drop_rate_float = 1.0
    rarest_drop_rate_fraction = None

    # Loop through all monsters in the database and print the monster name for each monster
    for monster in all_db_monsters:
        if monster.drops:
            for drop in monster.drops:
                if not drop.rarity:
                    continue
                drop_rate = eval(drop.rarity)
                rarest_drop[drop_rate].append(monster)
                if drop_rate < rarest_drop_rate_float:
                    rarest_drop_rate_float = drop_rate
                    rarest_drop_rate_fraction = drop.rarity

    print("%f" % rarest_drop_rate_float)
    print(rarest_drop_rate_fraction)
    for monster in rarest_drop[rarest_drop_rate_float]:
        print(monster.name)
