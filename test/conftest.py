"""
Author:  PH01L
Email:   phoil@osrsbox.com
Website: https://www.osrsbox.com

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


PROJECT_ROOT_PATH = Path(__file__).absolute().parent.parent
TEST_PATH = Path(PROJECT_ROOT_PATH / "test")


@pytest.fixture(scope="session")
def path_to_docs_dir() -> Path:
    return PROJECT_ROOT_PATH / "docs"


@pytest.fixture(scope="session")
def path_to_cache_dir() -> Path:
    return TEST_PATH / "cache"
