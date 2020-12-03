#!/bin/bash
: '
Author:  PH01L
Email:   phoil@osrsbox.com
Website: https://www.osrsbox.com

The primary entry script to update the osrsbox-db project after each weekly
in-game update.

The repos should already be cloned:
$ git clone https://github.com/runelite/runelite.git
$ git clone https://github.com/osrsbox/osrsbox-db.git

This script assumes the following packages:

- maven
- default-jdk
- python3
- git

To run:
$ ./update.sh

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
# Setup commonly used directories
odb=$(cd ..; pwd)
rl=$(cd ..; cd ..; cd runelite; pwd)

# Update all submodules
cd $odb
git submodule update --recursive --remote


# CACHE
# Build osrs-flatcache
echo -e ">>> Building osrs-cache..."
cd $odb/data/cache/osrs-flatcache
mvn clean
mvn install -Dcheckstyle.skip=false

# Find the packer.jar file with current version and bundled with dependencies
# For example: packer-1.6.10-shaded.jar
cd packer/target
jar_file=$(ls | grep .shaded.jar)

# Extract the flat cache
rm -rf $odb/data/cache/cache-data
mkdir -p $odb/data/cache/cache-data
java -jar $jar_file unpack $odb/data/cache/osrs-cache $odb/data/cache/cache-data


# RUNELITE
# Update RuneLite
echo -e ">>> Updating RuneLite..."
cd $rl
git pull

# Build using mvn command
echo -e ">>> Building RuneLite..."
mvn clean
mvn install -DskipTests

# Find the cache.jar file with current version and bundled with dependencies
# For example: cache-1.5.27-SNAPSHOT-jar-with-dependencies.jar
cd $rl/cache/target
jar_file=$(ls | grep .jar-with-dependencies.)

# Remove old cache dump
echo -e ">>> Removing the old cache dump in osrsbox-db..."
rm -r $odb/data/cache/items/
rm -r $odb/data/cache/npcs/
rm -r $odb/data/cache/objects/

# Dump the cache
echo -e ">>> Dumping cache using RuneLite cache tool..."
java -classpath $jar_file net.runelite.cache.Cache \
-cache $odb/data/cache/cache-data \
-items $odb/data/cache/items

java -classpath $jar_file net.runelite.cache.Cache \
-cache $odb/data/cache/cache-data \
-npcs $odb/data/cache/npcs

java -classpath $jar_file net.runelite.cache.Cache \
-cache $odb/data/cache/cache-data \
-objects $odb/data/cache/objects


# OSRSBOX
# Update osrsbox-db
echo -e ">>> Updating osrsbox-db..."
cd $odb
git pull

# Create virtual environment and activate
python3 -m venv venv
source venv/bin/activate

# Install Python package requirements
pip install -r requirements.txt

# Determine last wiki update timestamp
lastUpdate=$(date +%Y-%m-%dT%H:%M:%SZ -d "$(stat -c %x data/wiki/page-titles-items.json) - 2 days")

# Update wiki data for items/monsters
echo -e ">>> Updating wiki data..."
cd $odb/scripts/update/
python3 update_wiki_data.py $lastUpdate

# Generate the processed wikitext files
echo -e ">>> Process raw wikitext..."
cd $odb/scripts/wiki/
python3 process_wikitext.py

# Update items unalchable file
echo -e ">>> Update unalchable items..."
cd $odb/scripts/items/
python3 generate_items_unalchable.py

# # Update items buy limits file
# echo -e ">>> Update buy limits items..."
# cd $odb/scripts/items/
# python3 generate_items_buylimits.py

# Update local cache data from cache dump
echo -e ">>> Updating cache data..."
cd $odb/scripts/update/
python3 update_cache_data.py

# Determine cache changes
echo -e ">>> Determine any cache changes..."
cd $odb/scripts/update/
python3 determine_cache_changes.py

# Move the new cache data
cd $odb/
mv data/cache/items-cache-data.json data/items/
mv data/cache/monsters-cache-data.json data/monsters/

# Perform pre update_db.sh check for...
# item skill requirements, item weapon types, 
# item buy limits, and item icons
cd $odb/scripts/items/
echo -e ">>> Items with no weapon types..."
python3 check_item_weapon_types.py
echo -e ">>> Items with no buy limits..."
python3 check_item_buy_limits.py

cd $odb/scripts/icons/
echo -e ">>> Items with no icon..."
python3 check_item_icons.py

echo -e ">>> Updating item database"
cd $odb/builders/items/
python3 builder.py --export=True

echo -e ">>> Updating monster database"
cd $odb/builders/monsters/
python3 builder.py --export=True

echo -e ">>> Running JSON population scripts..."
cd $odb/scripts/update/
python3 update_json_files.py

echo -e ">>> Running repo tests..."
cd $odb
python3 -m flake8
python3 -m pytest test

# Make sure to deactivate the venv
deactivate
