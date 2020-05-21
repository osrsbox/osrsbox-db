#!/bin/bash
: '
Author:  PH01L
Email:   phoil@osrsbox.com
Website: https://www.osrsbox.com

The primary entry script to update the osrsbox-db project after each weekly
in-game update. This script assumes the following structure:
$ tree ~
/home/phoil
├── repos
│   ├── runelite
│   ├── osrsbox-db

The repos should already be populated:
$ git clone https://github.com/runelite/runelite.git
$ git clone https://github.com/osrsbox/osrsbox-db.git

This script assumes the following packages:

- default-jdk
- python3

To run:
$ pwd
/home/phoil/repos/osrsbox-db/scripts/
$ chmod u+x update_db.sh
$ ./update_db.sh

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
'

# Create virtual environment and activate
cd ~/repos/osrsbox-db
python3 -m venv venv
source venv/bin/activate

# Install Python package requirements
pip install -r requirements.txt

echo -e ">>> Updating item database"
cd ~/repos/osrsbox-db/builders/items/
python3 builder.py --export=True

echo -e ">>> Updating monster database"
cd ~/repos/osrsbox-db/builders/monsters/
python3 builder.py --export=True

echo -e ">>> Running JSON population scripts..."
cd ~/repos/osrsbox-db/scripts/update/
python3 update_json_files.py

echo -e ">>> Generating items-search.json file..."
cd ~/repos/osrsbox-db/scripts/items/
python3 generate_items_search_file.py

echo -e ">>> Running repo tests..."
cd ~/repos/osrsbox-db
python3 -m flake8
python3 -m pytest test

# Make sure to deactivate the venv
deactivate
