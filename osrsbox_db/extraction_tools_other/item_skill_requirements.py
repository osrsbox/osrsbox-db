# !/usr/bin/python

"""
Author:  PH01L
Email:   phoil@osrsbox.com
Website: osrsbox.com
Date:    2018/12/29

Description:
Simple caller script to print item names

Copyright (c) 2018, PH01L

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

>>> CHANGELOG:
    1.0.0       Base functionality
"""

__version__ = "1.0.0"

import json

from osrsbox_db.item_api_tools import AllItems


################################################################################
def determine_requirements(item_name):
    # Start with the desired skill
    options = {
        '0': None,
        '1': 'attack',
        '2': 'strength',
        '3': 'defence',
        '4': 'prayer',
        '5': "ranged",
        '6': 'magic',
        '7': '',
        '8': 'slayer',
        '9': 'agility',
        '10': 'firemaking',
        'x': 'exit'
        }
    print("0. None")
    print("1. Attack")
    print("2. Strength")
    print("3. Defence")
    print("4. Prayer")
    print("5. Ranged")
    print("6. Magic")
    print("7. Custom")
    print("8. Slayer")
    print("9. Agility")
    print("10. Firemaking")
    print("x. Exit")

    out_dict = dict()

    # Ask for the required skill (7 for multiple skills)
    skill_req_input = input(">>> SKILL: %s - " % item_name)

    # Exit check
    if skill_req_input == 'x':
        return None

    if skill_req_input == 'm':
        to_list = list()
        to_list.append({"skill_req": "attack", "level_req": 99})
        to_list.append({"skill_req": "strength", "level_req": 99})
        to_list.append({"skill_req": "defence", "level_req": 99})
        to_list.append({"skill_req": "hitpoints", "level_req": 99})
        to_list.append({"skill_req": "ranged", "level_req": 99})
        to_list.append({"skill_req": "prayer", "level_req": 99})
        to_list.append({"skill_req": "magic", "level_req": 99})
        to_list.append({"skill_req": "cooking", "level_req": 99})
        to_list.append({"skill_req": "woodcutting", "level_req": 99})
        to_list.append({"skill_req": "fletching", "level_req": 99})
        to_list.append({"skill_req": "fishing", "level_req": 99})
        to_list.append({"skill_req": "firemaking", "level_req": 99})
        to_list.append({"skill_req": "crafting", "level_req": 99})
        to_list.append({"skill_req": "smithing", "level_req": 99})
        to_list.append({"skill_req": "mining", "level_req": 99})
        to_list.append({"skill_req": "herblore", "level_req": 99})
        to_list.append({"skill_req": "agility", "level_req": 99})
        to_list.append({"skill_req": "theiving", "level_req": 99})
        to_list.append({"skill_req": "slayer", "level_req": 99})
        to_list.append({"skill_req": "farming", "level_req": 99})
        to_list.append({"skill_req": "runecrafting", "level_req": 99})
        to_list.append({"skill_req": "hunter", "level_req": 99})
        to_list.append({"skill_req": "contruction", "level_req": 99})
        out_dict["requirements"] = to_list
        return out_dict

    if skill_req_input == 'c':  # for a custom, not on the list
        skill_req_input = input(">>> SKILL: %s - " % item_name)
        skill_req = skill_req_input  # This breaks stuff
        level_req_input = input(">>> LEVEL: %s - " % item_name)
        level_req = int(level_req_input)
        to_list = list()
        to_list.append({"skill_req": skill_req, "level_req": level_req})
        out_dict["requirements"] = to_list
        return out_dict

    if skill_req_input == 't':  # for a custom, not on the list
        to_list = list()
        skill_req_input = input(">>> SKILL: %s - " % item_name)
        skill_req = options[skill_req_input]  # This breaks stuff
        level_req_input = input(">>> LEVEL: %s - " % item_name)
        level_req = int(level_req_input)
        to_list.append({"skill_req": skill_req, "level_req": level_req})
        skill_req_input = input(">>> SKILL: %s - " % item_name)
        skill_req = options[skill_req_input]  # This breaks stuff
        level_req_input = input(">>> LEVEL: %s - " % item_name)
        level_req = int(level_req_input)
        to_list.append({"skill_req": skill_req, "level_req": level_req})
        skill_req_input = input(">>> SKILL: %s - " % item_name)
        skill_req = options[skill_req_input]  # This breaks stuff
        level_req_input = input(">>> LEVEL: %s - " % item_name)
        level_req = int(level_req_input)
        to_list.append({"skill_req": skill_req, "level_req": level_req})
        out_dict["requirements"] = to_list
        return out_dict

    if skill_req_input == '0':
        out_dict["requirements"] = None
        return out_dict

    if skill_req_input != '7':
        # Fetch formatted skill requirement from options dict
        skill_req = options[skill_req_input]
        # Ask for level requirement, if no skill requirement, level requirement is None
        if skill_req:
            level_req = None
        else:
            level_req_input = input(">>> LEVEL: %s - " % item_name)
            level_req = int(level_req_input)
        to_list = list()
        to_list.append({"skill_req": skill_req, "level_req": level_req})
        out_dict["requirements"] = to_list
        return out_dict

    if skill_req_input == '7':
        # Fetch formatted skill requirement from options dict
        skill_req_input = input(">>> SKILL: %s - " % item_name)
        first_skill_req = skill_req_input  # This breaks stuff
        level_req_input = input(">>> LEVEL: %s - " % item_name)
        first_level_req = int(level_req_input)

        skill_req_input = input(">>> SKILL: %s - " % item_name)
        second_skill_req = skill_req_input
        level_req_input = input(">>> LEVEL: %s - " % item_name)
        second_level_req = int(level_req_input)

        out_dict["requirements"] = [{"skill_req": first_skill_req, "level_req": first_level_req},
                                    {"skill_req": second_skill_req, "level_req": second_level_req}]
        return out_dict


def clean(input):
    # input = input.replace(" 100", "")
    # input = input.replace(" 75", "")
    # input = input.replace(" 50", "")
    # input = input.replace(" 25", "")
    # input = input.replace(" (g)", "")
    # input = input.replace(" (t)", "")
    # input = input.replace("(t)", "")
    # input = input.replace(" (p)", "")
    # input = input.replace(" (p+)", "")
    # input = input.replace(" (p++)", "")
    # input = input.replace("(kp)", "")
    # input = input.replace("(p)", "")
    # input = input.replace("(p+)", "")
    # input = input.replace("(p++)", "")
    # input = input.replace(" (10)", "")
    # input = input.replace(" (9)", "")
    # input = input.replace(" (8)", "")
    # input = input.replace(" (7)", "")
    # input = input.replace(" (6)", "")
    # input = input.replace(" (5)", "")
    # input = input.replace(" (4)", "")
    # input = input.replace(" (3)", "")
    # input = input.replace(" (2)", "")
    # input = input.replace(" (1)", "")
    # input = input.replace("(10)", "")
    # input = input.replace("(9)", "")
    # input = input.replace("(8)", "")
    # input = input.replace("(7)", "")
    # input = input.replace("(6)", "")
    # input = input.replace("(5)", "")
    # input = input.replace("(4)", "")
    # input = input.replace("(3)", "")
    # input = input.replace("(2)", "")
    # input = input.replace("(1)", "")
    # input = input.replace(" 9/10", " full")
    # input = input.replace(" 8/10", " full")
    # input = input.replace(" 7/10", " full")
    # input = input.replace(" 6/10", " full")
    # input = input.replace(" 5/10", " full")
    # input = input.replace(" 4/10", " full")
    # input = input.replace(" 3/10", " full")
    # input = input.replace(" 2/10", " full")
    # input = input.replace(" 1/10", " full")
    # input = input.replace(" (h1)", " full")
    # input = input.replace(" (h2)", " (h1)")
    # input = input.replace(" (h3)", " (h1)")
    # input = input.replace(" (h4)", " (h1)")
    # input = input.replace(" (h5)", " (h1)")
    # input = input.replace(" (e)", "")
    # input = input.replace(" (t6)", "")
    # input = input.replace(" (t5)", "")
    # input = input.replace(" (t4)", "")
    # input = input.replace(" (t3)", "")
    # input = input.replace(" (t2)", "")
    # input = input.replace(" (t1)", "")
    # input = input.replace("Elite void robe", "Void knight top")
    # input = input.replace(" (i)", "")
    # input = input.replace("(i)", "")
    return input


################################################################################
if __name__ == "__main__":
    import argparse
    ap = argparse.ArgumentParser()
    ap.add_argument("-i",
                    "--input",
                    required=True,
                    help="Two options: 1) Directory of JSON item files (../docs/items-json), or 2) Single JSON file (../docs/items_complete.json) ")
    args = vars(ap.parse_args())

    # Start processing all items in database
    ai = AllItems.AllItems(args["input"])

    # Load current file
    isr_file = "item_skill_requirements.json"
    known_items = dict()
    with open(isr_file) as f:
        known_items = json.load(f)

    done = list()
    for i in known_items:
        done.append(i)

    for item in ai:
        if str(item.id) in done:
            # Item ID is already done, skip to next
            continue
        if item.equipable:
            # If item is equipable and not process, process it!
            clean_name = clean(item.name)
            requirements = determine_requirements(item.name)
            if requirements:
                known_items[item.id] = None
            elif requirements["requirements"]:
                known_items[item.id] = requirements["requirements"]
            else:
                known_items[item.id] = requirements["requirements"]

    # Finally, save any changes
    with open(isr_file, "w") as f:
        json.dump(known_items, f, indent=4)
