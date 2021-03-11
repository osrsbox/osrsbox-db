"""
Author:  PH01L
Email:   phoil@osrsbox.com
Website: https://www.osrsbox.com

Description:
Fetch a list of item buy limits from the OSRS Wiki.

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
import re
import json
from pathlib import Path

import requests

import config


def fetch():
    # Fetch the OSRS Wiki buy limits module data
    url = "https://oldschool.runescape.wiki/w/Module:GELimits/data?action=raw"

    try:
        data = requests.get(url, headers=config.custom_agent).text
    except requests.exceptions.RequestException as e:
        raise SystemExit(">>> ERROR: Get request error. Exiting.") from e

    buy_limits = dict()

    # Parse each line, looking for following structure
    # ["3rd age amulet"] = 8,
    # Source: runelite/runelite-wiki-scraper
    for line in data.split("\n"):
        match = re.search(r"\[\"(.*)\"\] = (\d+),?", str(line))
        if match:
            name = match.group(1).replace('\\', '')
            limit = match.group(2)
            buy_limits[name] = int(limit)

    file_name = "items-buylimits.json"
    file_path = Path(config.DATA_ITEMS_PATH / file_name)
    with open(file_path, "w") as f:
        json.dump(buy_limits, f, indent=4)


if __name__ == "__main__":
    fetch()
