"""
Author:  PH01L
Email:   phoil@osrsbox.com
Website: https://www.osrsbox.com

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
import json

import mwparserfromhell

from monsters_builder import monster_builder


def map_npcs_from_cache_to_wiki(monster_name, wiki_text, attackable_npcs):
    monster_ids = dict()
    monster_template = None  # Current template
    monster_templates = list()  # List of all templates

    # Parse wiki text and get "Infoxbox Monster" templates
    wiki_code = mwparserfromhell.parse(wiki_text)
    templates = wiki_code.filter_templates()
    for template in templates:
        template_name = template.name.strip()
        template_name = template_name.lower()
        if "infobox monster" in template_name:  # There can be two of these
            monster_template = True
            monster_templates.append(template)

    # Couldn't find template an "Infoxbox Monster"
    if monster_template is None:
        return

    # Loop the "Infoxbox Monster" templates, determine number of versions
    # This uses "id", "id1", "id2", "id3" etc as a key
    for monster_template in monster_templates:
        version_count = 0
        try:
            monster_template.get("id" + "1").value
            # Try to determine how many versions are present
            i = 1
            while i <= 20:  # Guessing max version number is 20
                try:
                    monster_template.get("id" + str(i)).value
                    version_count += 1
                except ValueError:
                    break
                i += 1
        except ValueError:
            pass

        # Process single, or versioned "Infoxbox Monster" template/s
        if version_count == 0:
            try:
                ids = monster_template.get("id").value
                ids = ids.strip()
                ids = ids.split(",")
                for id in ids:
                    monster_ids[id] = [monster_name, wiki_text, monster_template, version_count]
            except ValueError:
                print("WARNING: No ID number:", monster_name)
        else:
            i = 1
            while i <= version_count:
                try:
                    ids = monster_template.get("id" + str(i)).value
                    ids = ids.strip()
                    ids = ids.split(",")
                    for id in ids:
                        monster_ids[id] = [monster_name, wiki_text, monster_template, i]
                    i += 1
                except ValueError:
                    print("WARNING: No ID number:", monster_name)
                    i += 1

    return monster_ids


if __name__ == "__main__":
    # Delete old log file
    if os.path.exists("builder.log"):
        os.remove("builder.log")

    # Set data input directories
    paths_wiki = os.path.join("..", "extraction_tools_wiki", "")
    paths_other = os.path.join("..", "extraction_tools_other", "")
    paths_data = os.path.join("..", "data", "")
    paths_docs = os.path.join("..", "docs", "")

    # Load the raw output from OSRS cache
    with open(paths_data + "attackable-npcs.json") as f:
        attackable_npcs = json.load(f)

    # Load the wiki text file
    with open(paths_wiki + "extract_page_text_monsters.json") as wiki_text_file:
        wiki_text = json.load(wiki_text_file)

    # STAGE ONE: Start correlation between the OSRS cache data, and OSRS Wiki data

    found_ids = dict()
    print(">>> Starting ID correlation...")
    # Loop OSRS Wiki entries from monster category
    for monster_name, wiki_text in wiki_text.items():
        monster_ids = map_npcs_from_cache_to_wiki(monster_name, wiki_text, attackable_npcs)
        if monster_ids:
            for monster_id, data in monster_ids.items():
                found_ids[monster_id] = data

    to_process = dict()  # monster id : cache_name, wiki_name, wiki_text,

    print(">>> Populating attackable NPCs data...")
    # Match attackable NPCs with wiki data
    attackable_npcs_list = sorted(attackable_npcs, key=lambda x: int(x))
    for monster_def_id in attackable_npcs_list:
        cache_def = attackable_npcs[monster_def_id]
        try:
            cache_name = cache_def["name"]
            cache_combat_level = cache_def["combatLevel"]
            wiki_name = found_ids[monster_def_id][0]
            wiki_text_data = found_ids[monster_def_id][1]
            monster_template = found_ids[monster_def_id][2]
            infobox_version = found_ids[monster_def_id][3]
            to_process[monster_def_id] = {
                "cache_name": cache_name,
                "wiki_name": wiki_name,
                "wiki_text": wiki_text_data,
                "template": monster_template,
                "infobox_version": infobox_version,
                "cache_combat_level": cache_combat_level
            }
        except KeyError:
            print("ERROR", monster_def_id, cache_def["name"], cache_def["combatLevel"])

    print(">>> Starting to build the monster database...")
    # Start processing every monster!
    for monster_id in to_process:
        # Initialize the BuildMonster class
        builder = monster_builder.BuildMonster(monster_id,
                                               to_process[monster_id])
        # Start the build monster population function
        builder.populate()
