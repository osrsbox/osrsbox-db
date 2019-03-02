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

import datetime

import dateparser


def clean_boolean(value: str) -> bool:
    """A helper method to convert the members entry from an OSRS Wiki infobox.

    :param value: The extracted raw wiki text.
    :return tradeable: A cleaned members property of an item.
    """
    value = str(value)

    if value is None:
        return None

    value = value.strip()
    value = value.replace("[", "")
    value = value.replace("]", "")

    if value in ["True", "true", True, "Yes", "yes"]:
        value = True
    elif value in ["False", "false", False, "No", "no"]:
        value = False
    else:
        value = False

    return value


def clean_release_date(value: str) -> str:
    """A helper method to convert the release date entry from an OSRS Wiki infobox.

    The returned value will be a specifically formatted string: dd Month YYYY.
    For example, 25 June 2017 or 01 November 2014.

    :param value: The extracted raw wiki text.
    :return release_date: A cleaned release date of an item.
    """
    release_date = str(value)

    if release_date is None:
        return None

    release_date = release_date.strip()
    release_date = release_date.replace("[", "")
    release_date = release_date.replace("]", "")

    try:
        release_date = datetime.datetime.strptime(release_date, "%d %B %Y")
        return release_date.strftime("%d %B %Y")
    except ValueError:
        pass

    try:
        release_date = dateparser.parse(release_date)
        release_date = release_date.strftime("%d %B %Y")
    except (ValueError, TypeError, AttributeError):
        return None

    return release_date


def clean_combat_level(value: str) -> int:
    """A helper method to convert the release date entry from an OSRS Wiki infobox.

    The returned value will be a specifically formatted string: dd Month YYYY.
    For example, 25 June 2017 or 01 November 2014.

    :param value: The extracted raw wiki text.
    :return release_date: A cleaned release date of an item.
    """
    # Handle: None, empty string, N/A string
    if value is None or "N/A" in value or value == "":
        return None

    # For: https://oldschool.runescape.wiki/w/Mummy#Lv_96
    # {{*}} 96<br>'''Alight:'''<br>{{*}} 98
    if "<br>" in value:
        value = value.split("<br>")[0]
        value = value.replace("{{*}}", "")
    if "<br/>" in value:
        value = value.split("<br/>")[0]
        value = value.replace("{{*}}", "")

    # For: https://oldschool.runescape.wiki/w/Great_Olm
    # 549<ref name="variedstats"></ref>
    value = value.split('<ref')[0]

    # Handle comma-separated combat levels
    # Example: https://oldschool.runescape.wiki/w/Unicorn
    if "," in value:
        value = value.split(",")[0]

    combat_level = int(value)
    return combat_level


def clean_hitpoints(value: str) -> int:
    """"""
    # Handle: None, empty string, N/A string
    if value is None or "N/A" in value or value == "":
        return None

    # Handle comment in value
    if "<!--" in value:
        value = value.split("<!--")[0]

    # Handlle "Varies"
    # Example: https://oldschool.runescape.wiki/w/Portal_(Pest_Control)
    # Varies (200, 250)
    if "Varies" in value:
        value = value.split("(")[1]
        value = value.split(",")[0]  # This solution grabs the first value in the tuple

    # Handle another varies
    # Example: https://oldschool.runescape.wiki/w/Koschei_the_deathless
    # 79(255)
    if "(" in value:
        value = value.split("(")[0]

    hitpoints = int(value)
    return hitpoints
