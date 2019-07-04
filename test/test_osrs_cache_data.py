"""
Author:  PH01L
Email:   phoil@osrsbox.com
Website: https://www.osrsbox.com

Description:
Tests for module: extraction_tools_cache.osrs_cache_data module

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

import pytest
from pathlib import Path

from extraction_tools_cache import osrs_cache_data


@pytest.mark.parametrize("test_data,expected", [
    ({"id": 7410, "name": "Greater abyssal demon", "models": [32921]},
     "eJyrVspMUbJSMDcxNNBRUMpLzE0F8pTci1ITS1KLFBKTKouLE3MUUlJz8/OUgApy81NSc4qBSqKNjSyNDGNrAWB5EzI=")
])
def test_osrs_cache_data_compression(test_data, expected):
    id_number, json_out = osrs_cache_data.compress_definition_file(test_data)
    assert json_out == expected


@pytest.mark.parametrize("cache_type,expected", [
    ("items", 23531),
    ("npcs", 8721),
    ("objects", 34905)
])
def test_osrs_cache_data_decompression(path_to_cache_dir: Path, cache_type, expected):
    path_to_cache_file = path_to_cache_dir / f"{cache_type}.json"
    definitions = osrs_cache_data.CacheDefinitionFiles(path_to_cache_file)
    definitions.decompress_cache_file()
    assert len(definitions) == expected
