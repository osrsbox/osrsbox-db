"""
Author:  PH01L
Email:   phoil@osrsbox.com
Website: https://www.osrsbox.com

Description:
Update MongoDB with changes.

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
import json
from pathlib import Path

from pymongo import MongoClient

import config
from scripts.cache import cache_constants

# Set MongoDB connection configuration
ip_address = "localhost"
port = 27017
db_name = "osrsbox-db"

# Initialize MongoDB connection
print(">>> Connecting to MongoDB database....")
client = MongoClient(ip_address, port)

# Load database
db = client[db_name]

collection_names = [
    "items",
    "monsters",
    "cache-items",
    "cache-npcs",
    "cache-objects"
]

# Updating each collection
print(">>> Loading MongoDB collections....")
for collection_name in collection_names:
    print(f"  > Loading collection: {collection_name}")

    # Specify collection to update
    collection_items = db[collection_name]

    if collection_name.startswith("cache"):
        # Load collection file (cache data)
        if collection_name == "cache-items":
            data = cache_constants.ITEM_DEFINITIONS
        elif collection_name == "cache-npcs":
            data = cache_constants.NPC_DEFINITIONS
        elif collection_name == "cache-objects":
            data = cache_constants.OBJECT_DEFINITIONS
    else:
        # Load collection file (items-complete.json or monsters-complete.json)
        data_file_path = Path(config.DOCS_PATH / f"{collection_name}-complete.json")
        # Open and load file
        with open(data_file_path) as f:
            data = json.load(f)

    # Loop each entry in data file
    count = 0
    for new_entry_dict in data.values():
        if count % 2000 == 0:
            print(f"  > Processing: {count}")
        # Set MongoDB _id property
        new_entry_dict["_id"] = new_entry_dict["id"]

        # Determine if entry exists in MongoDB
        existing_entry_dict = collection_items.find_one({"_id": new_entry_dict["id"]})

        # Populate entry
        if existing_entry_dict:
            collection_items.replace_one(existing_entry_dict, new_entry_dict, upsert=True)
        else:
            collection_items.insert_one(new_entry_dict)

        count += 1
