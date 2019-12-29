"""
Author:  PH01L
Email:   phoil@osrsbox.com
Website: https://www.osrsbox.com

Description:
Initialize MongoDB - create and configure database and collections. Also
add any validation using projects schemas.

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

from pymongo import errors
from pymongo import MongoClient

import config


# Set MongoDB connection configuration
ip_address = "localhost"
port = 27017
db_name = "osrsbox-db"

# Initialize MongoDB connection
print(">>> Connecting to MongoDB database....")
client = MongoClient(ip_address, port)

# Drop existing database
client.drop_database(db_name)

# Load database
db = client[db_name]

collection_names = [
    "items",
    "monsters",
    "cache-items",
    "cache-npcs",
    "cache-objects"
]

# Load each collection
print(">>> Loading MongoDB collections....")
for collection_name in collection_names:
    print(f"  > Loading collection: {collection_name}")

    # Create a collection, if it doesn't exist
    try:
        db.create_collection(collection_name)
    except errors.CollectionInvalid:
        pass

    collection = client[collection_name]

    # Add validation for collection
    schema_file = Path(config.DATA_SCHEMAS_PATH / f"schema-{collection_name}.json")

    print(f">>> Processing: {schema_file}")

    with open(schema_file) as f:
        data = json.load(f)

    # Start populating headers in the JSON schema
    json_out = dict()
    json_out["$jsonSchema"] = dict()
    json_out["$jsonSchema"]["bsonType"] = "object"
    json_out["$jsonSchema"]["properties"] = data["properties"]

    query = [
        ("collMod", collection_name),
        ("validator", json_out),
        ("validationLevel", "strict")
    ]
    query = dict(query)

    db.command(query)
