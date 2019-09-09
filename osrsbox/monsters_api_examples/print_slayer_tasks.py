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


slayer_masters_assignments = {
    "chaeldar": set(),
    "konar": set(),
    "turael": set(),
    "mazchna": set(),
    "vannaka": set(),
    "krystilia": set(),
    "duradel": set(),
    "nieve": set()
}

if __name__ == "__main__":
    # Load all monsters
    all_db_monsters = monsters_api.load()

    # Loop through all monsters in the database
    monster_set = set()
    for monster in all_db_monsters:
        if monster.slayer_monster:
            for slayer_master in monster.slayer_masters:
                slayer_masters_assignments[slayer_master].add(monster.name)

    for slayer_master, assignments in slayer_masters_assignments.items():
        print(slayer_master)
        print(assignments)
