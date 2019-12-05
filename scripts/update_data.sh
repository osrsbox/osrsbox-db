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
mvn clean
mvn install -DskipTests

# Find the cache.jar file with current version and bundled with dependencies
# For example: cache-1.5.27-SNAPSHOT-jar-with-dependencies.jar
cd ~/repos/runelite/cache/target
jar_file=$(ls | grep .jar-with-dependencies.)

# Remove old cache dump
echo -e ">>> Removing the old cache dump in osrsbox-db..."
rm -r ~/repos/osrsbox-db/extraction_tools_cache/items/
rm -r ~/repos/osrsbox-db/extraction_tools_cache/npcs/
rm -r ~/repos/osrsbox-db/extraction_tools_cache/objects/

# Dump the cache
echo -e ">>> Dumping cache using RuneLite cache tool..."
java -classpath $jar_file net.runelite.cache.Cache \
-cache ~/jagexcache/oldschool/LIVE \
-items ~/repos/osrsbox-db/extraction_tools_cache/items

java -classpath $jar_file net.runelite.cache.Cache \
-cache ~/jagexcache/oldschool/LIVE \
-npcs ~/repos/osrsbox-db/extraction_tools_cache/npcs

java -classpath $jar_file net.runelite.cache.Cache \
-cache ~/jagexcache/oldschool/LIVE \
-objects ~/repos/osrsbox-db/extraction_tools_cache/objects


# OSRSBOX
# Update osrsbox-db
echo -e ">>> Updating osrsbox-db..."
cd ~/repos/osrsbox-db
git pull

# Move to the scripts/ path and update all data
cd ~/repos/osrsbox-db/scripts/

echo -e ">>> Updating wiki data..."
python3 update_wiki_data.py 2019-11-28T00:00:00Z

echo -e ">>> Updating cache data..."
python3 update_cache_data.py

echo -e ">>> Determine any cache changes..."
python3 determine_cache_changes.py

# Move the new cache data
cd ~/repos/osrsbox-db/
mv extraction_tools_cache/items-cache-data.json data/
mv extraction_tools_cache/monsters-cache-data.json data/

# Generate the processed wikitext files
echo -e ">>> Process raw wikitext..."
cd ~/repos/osrsbox-db/extraction_tools_wiki/
python3 process_wikitext.py

echo -e ">>> FINISHED DATA UPDATE... MAKE SURE TO..."
echo -e ">>> Update changelog"
echo -e ">>> Update tests"
