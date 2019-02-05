"""
Author:  PH01L
Email:   phoil@osrsbox.com
Website: https://www.osrsbox.com

Description:
Tests for module: extraction_tools_cache.extract_model_ids

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

import os
from pathlib import Path

from extraction_tools_cache import osrs_cache_data
from extraction_tools_cache import extract_model_ids


def test_osrs_cache_extract_model_ids(path_to_cache_dir: Path):
    for cache_file in extract_model_ids.CACHE_DUMP_FILES:
        # Set the path to the compressed JSON files
        compressed_json_file = os.path.join(path_to_cache_dir, cache_file)
        # Load the compressed file and parse using the osrs_cache_data module
        definitions = osrs_cache_data.CacheDefinitionFiles(compressed_json_file)

        if cache_file == "items.json":
            # Get the JSON data for the "Kyatt legs" item
            json_data = definitions["10035"]

            # Test the model extraction function
            model_data = extract_model_ids.extract_model_ids(json_data, "items")[0]
            assert model_data["type"] == "items"
            assert model_data["type_id"] == 10035
            assert model_data["name"] == "Kyatt legs"
            assert model_data["model_id"] == 19453

        elif cache_file == "npcs.json":
            # Get the JSON data for the "Black dragon" item
            json_data = definitions["258"]

            # Test the model extraction function
            model_data = extract_model_ids.extract_model_ids(json_data, "npcs")[0]
            assert model_data["type"] == "npcs"
            assert model_data["type_id"] == 258
            assert model_data["name"] == "Black dragon"
            assert model_data["model_id"] == 17423

        elif cache_file == "objects.json":
            # Get the JSON data for the "Dead Snape grass" item
            json_data = definitions["33690"]

            # Test the model extraction function
            model_data = extract_model_ids.extract_model_ids(json_data, "objects")[0]
            assert model_data["type"] == "objects"
            assert model_data["type_id"] == 33690
            assert model_data["name"] == "Dead Snape grass"
            assert model_data["model_id"] == 7766
