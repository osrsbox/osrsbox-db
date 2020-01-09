"""
Author:  PH01L
Email:   phoil@osrsbox.com
Website: https://www.osrsbox.com

Description:
Automatically generate JSON schemas for cache definitions.

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
from typing import Dict

import config
from scripts.cache import cache_constants


def generate_cache_schema(cache_definition: Dict, cache_dump_type: str):
    """Generate a JSON schema for a OSRS cache definition.

    :param cache_definitions: A JSON cache file as a Python dict.
    :param cache_dump_type: The type of cache (items, npcs, or objects).
    """
    json_out = dict()
    required = list()

    # Start populating headers in the JSON scehma
    json_out["$schema"] = "http://json-schema.org/draft-07/schema#"
    json_out["description"] = f"JSON Schema for an OSRS {cache_dump_type} definition."
    json_out["title"] = f"OSRS Cache - {cache_dump_type}."
    json_out["type"] = "object"
    json_out["properties"] = dict()

    # Look keys/values in defintion and set type
    for k, v in cache_definition.items():
        json_out["properties"][k] = dict()
        if isinstance(v, str):
            json_out["properties"][k]["type"] = "string"
        elif isinstance(v, bool):
            json_out["properties"][k]["type"] = "boolean"
        elif isinstance(v, int):
            json_out["properties"][k]["type"] = "number"
        elif isinstance(v, float):
            json_out["properties"][k]["type"] = "number"
        elif isinstance(v, list):
            json_out["properties"][k]["type"] = "array"

        # Add key to the array (list) of required properties
        required.append(k)

    # Add required array (list) to the schema
    json_out["required"] = required

    # Dump the generated JSON schema
    out_fi_path = Path(config.DATA_SCHEMAS_PATH / f"schema-cache-{cache_dump_type}.json")
    with open(out_fi_path, "w") as f:
        json.dump(json_out, f, indent=4)


def main():
    """The main entry point for the program."""
    # Loop cache types (items, npcs, objects)
    for cache_dump_type in cache_constants.CACHE_DUMP_TYPES:
        print(f">>> Processing: {cache_dump_type}")

        # Load cache file to process
        cache_file = Path(config.DATA_CACHE_PATH / cache_dump_type / "1.json")

        if not cache_file.exists():
            print(">>> Error: Cannot find cache files. Exiting.")
            exit(1)

        with open(cache_file) as f:
            data = json.load(f)
            # Generate the schema
            generate_cache_schema(data, cache_dump_type)


if __name__ == "__main__":
    main()
