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

- maven
- default-jdk
- python3
- git

To run:
$ pwd
/home/phoil/repos/osrsbox-db/scripts/
$ chmod u+x update_data.sh
$ ./update_data.sh

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

# RUNELITE
# Update RuneLite
echo -e ">>> Updating RuneLite..."
cd ~/repos/runelite
git pull

echo -e ">>> Building RuneLite..."
# Build using mvn command
mvn clean
mvn install -DskipTests

# Find the cache.jar file with current version and bundled with dependencies
# For example: cache-1.5.27-SNAPSHOT-jar-with-dependencies.jar
cd ~/repos/runelite/cache/target
jar_file=$(ls | grep .jar-with-dependencies.)

# Remove old cache dump
echo -e ">>> Removing the old cache dump in osrsbox-db..."
rm -r ~/repos/osrsbox-db/data/cache/items/
rm -r ~/repos/osrsbox-db/data/cache/npcs/
rm -r ~/repos/osrsbox-db/data/cache/objects/

# Dump the cache
echo -e ">>> Dumping cache using RuneLite cache tool..."
java -classpath $jar_file net.runelite.cache.Cache \
-cache ~/jagexcache/oldschool/LIVE \
-items ~/repos/osrsbox-db/data/cache/items

java -classpath $jar_file net.runelite.cache.Cache \
-cache ~/jagexcache/oldschool/LIVE \
-npcs ~/repos/osrsbox-db/data/cache/npcs

java -classpath $jar_file net.runelite.cache.Cache \
-cache ~/jagexcache/oldschool/LIVE \
-objects ~/repos/osrsbox-db/data/cache/objects

# OSRSBOX
# Update osrsbox-db
echo -e ">>> Updating osrsbox-db..."
cd ~/repos/osrsbox-db
git pull

# Create virtual environment and activate
python3 -m venv venv
source venv/bin/activate

# Install Python package requirements
pip install -r requirements.txt

# Update wiki data for items/monsters
echo -e ">>> Updating wiki data..."
cd ~/repos/osrsbox-db/scripts/update/
python3 update_wiki_data.py 2020-07-15T00:00:00Z

# Generate the processed wikitext files
echo -e ">>> Process raw wikitext..."
cd ~/repos/osrsbox-db/scripts/wiki/
python3 process_wikitext.py

# Update items unalchable file
echo -e ">>> Update unalchable items..."
cd ~/repos/osrsbox-db/scripts/items/
python3 generate_items_unalchable.py

# Update local cache data from cache dump
echo -e ">>> Updating cache data..."
cd ~/repos/osrsbox-db/scripts/update/
python3 update_cache_data.py

# Determine cache changes
echo -e ">>> Determine any cache changes..."
cd ~/repos/osrsbox-db/scripts/update/
python3 determine_cache_changes.py

# Move the new cache data
cd ~/repos/osrsbox-db/
mv data/cache/items-cache-data.json data/items/
mv data/cache/monsters-cache-data.json data/monsters/

# Perform pre update_db.sh check for...
# item skill requirements, item weapon types, 
# item buy limits, and item icons
cd ~/repos/osrsbox-db/scripts/items/
echo -e ">>> Items with no skill requirements..."
python3 check_item_skill_requirements.py
echo -e ">>> Items with no weapon types..."
python3 check_item_weapon_types.py
echo -e ">>> Items with no buy limits..."
python3 check_item_buy_limits.py

cd ~/repos/osrsbox-db/scripts/icons/
echo -e ">>> Items with no icon..."
python3 check_item_icons.py

# Make sure to deactivate the venv
deactivate
