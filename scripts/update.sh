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
$ chmod u+x update.sh
$ ./update.sh

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
'

# RUNELITE
# Update RuneLite
echo -e ">>> Updating RuneLite..."
cd ~/repos/runelite
git pull

echo -e ">>> Building RuneLite..."
# Build using mvn command
mvn install -DskipTests

# Find the cache.jar file with current version and bundled with dependencies
# For example: cache-1.5.27-SNAPSHOT-jar-with-dependencies.jar
cd ~/repos/runelite/cache/target
jar_file=$(ls | grep *jar-with-dependencies*)

# Remove old cache dump
echo -e ">>> Removing the old cache dump in osrsbox-db..."
rm -r ~/repos/osrsbox-db/extraction_tools_cache/items
rm -r ~/repos/osrsbox-db/extraction_tools_cache/npcs
rm -r ~/repos/osrsbox-db/extraction_tools_cache/objects

# Dump the cache
echo -e ">>> Dumping cache using RuneLite cache tool..."
java -jar $jar_file \
     -cp net.runelite.cache.Cache \
     -c ~/jagexcache/oldschool/LIVE \
     -items ~/osrsbox-db/extraction_tools_cache/items
java -jar $jar_file \
     -cp net.runelite.cache.Cache \
     -c ~/jagexcache/oldschool/LIVE \
     -npcs ~/osrsbox-db/extraction_tools_cache/npcs
java -jar $jar_file \
     -cp net.runelite.cache.Cache \
     -c ~/jagexcache/oldschool/LIVE \
     -obejcts ~/osrsbox-db/extraction_tools_cache/obejcts


# OSRSBOX
# Update, and deploy osrsbox-db
echo -e ">>> Updating osrsbox-db..."
cd ~/repos/osrsbox-db
git pull

# Move to the scripts/update_items path and update everything
cd ~/repos/osrsbox-db/scripts/
echo -e ">>> Updating cache data..."
python3 update_cache_data.py
echo -e ">>> Updating wiki data..."
python3 update_wiki_data.py

echo -e ">>> Determine any newly added items..."
cd ~/repos/osrsbox-db/scripts/update_items
python3 determine_new_items.py

echo -e ">>> Updating item database"
cd ~/repos/osrsbox-db/items_builder
python3 builder.py

echo -e ">>> Runing item population scripts..."
cd ~/repos/osrsbox-db/scripts/update_items
python3 generate_items_complete.py
python3 generate_items_slot_files.py

# Print remaining tasks to user...
echo -e ">>> REMEMBER YOU STILL NEED TO DO THE FOLLOWING..."
echo -e ">>> 0) Update changelog"
echo -e ">>> 1) Update tests"
echo -e ">>> 2) Run pytests"
echo -e ">>> 3) Increment PyPi package (if required)"
echo -e ">>> 4) Update PyPi README.md"
echo -e ">>> 5) git push"
