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

import pytest
from pathlib import Path

from extraction_tools_cache import osrs_cache_data
from extraction_tools_cache import extract_summary_model_ids


@pytest.mark.parametrize("definition_id,cache_type,expected", [
    ("10035", "items", 19453),
    ("258", "npcs", 17423),
    ("33690", "objects", 7766)
])
def test_osrs_cache_extract_model_ids(path_to_cache_dir: Path, definition_id, cache_type, expected):
    path_to_cache_file = path_to_cache_dir / f"{cache_type}.json"
    definitions = osrs_cache_data.CacheDefinitionFiles(path_to_cache_file)
    definitions.decompress_cache_file()
    json_data = definitions[definition_id]
    model_data = extract_summary_model_ids.extract_model_ids(json_data, cache_type)[0]
    assert model_data["model_id"] == expected
