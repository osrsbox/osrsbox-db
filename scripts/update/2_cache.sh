#!/bin/bash
: '
Author:  PH01L
Email:   phoil@osrsbox.com
Website: https://www.osrsbox.com

Update flatcache and extract cache data.

Copyright (c) 2021, PH01L

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
rl=$(cd ../../..; cd runelite; pwd)

echo -e ">>> flatcache..."
echo -e "  > Building osrs-flatcache..."
cd $odb/data/cache/osrs-flatcache
mvn clean
mvn install -Dcheckstyle.skip=false

# Find the packer.jar file with current version and bundled with dependencies
# For example: packer-1.6.10-shaded.jar
cd packer/target
jar_file=$(ls | grep .shaded.jar)

echo -e "  > Extracting osrs-cache..."
rm -rf $odb/data/cache/cache-data
mkdir -p $odb/data/cache/cache-data
java -jar $jar_file unpack $odb/data/cache/osrs-cache $odb/data/cache/cache-data

echo -e ">>> runelite..."
cd $rl
git pull

echo -e "  > Building RuneLite..."
mvn clean
mvn install -DskipTests

# Find the cache.jar file with current version and bundled with dependencies
# For example: cache-1.5.27-SNAPSHOT-jar-with-dependencies.jar
cd $rl/cache/target
jar_file=$(ls | grep .jar-with-dependencies.)

# Remove old cache dumps
echo -e "  > Removing the old cache dump in osrsbox-db..."
rm -r $odb/data/cache/items/
rm -r $odb/data/cache/npcs/
rm -r $odb/data/cache/objects/

# Dump the cache
echo -e "  > Dumping cache using RuneLite cache tool..."
java -classpath $jar_file net.runelite.cache.Cache \
-cache $odb/data/cache/cache-data \
-items $odb/data/cache/items

java -classpath $jar_file net.runelite.cache.Cache \
-cache $odb/data/cache/cache-data \
-npcs $odb/data/cache/npcs

java -classpath $jar_file net.runelite.cache.Cache \
-cache $odb/data/cache/cache-data \
-objects $odb/data/cache/objects
