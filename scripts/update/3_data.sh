#!/bin/bash
: '
Author:  PH01L
Email:   phoil@osrsbox.com
Website: https://www.osrsbox.com

Process cache data, then fetch wiki data.

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
odb=$(cd ../..; pwd)

export PYTHONPATH="$(dirname "$(dirname "$(pwd)")")"

echo -e ">>> Updating project data..."
cd $odb
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt

echo -e "  > cache..."
cd $odb/scripts/cache
python3 update.py

echo -e "  > items..."
cd $odb/scripts/items
python3 update.py
cd $odb/scripts/icons
python3 convert_item_icons.py

echo -e "  > monsters..."
cd $odb/scripts/monsters
python3 update.py
