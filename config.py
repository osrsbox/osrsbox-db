"""
Author:  PH01L
Email:   phoil@osrsbox.com
Website: https://www.osrsbox.com

Description:
Global project configurations including project path constants and
Cerberus validator configuration.

Copyright (c) 2020, PH01L

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
from pathlib import Path

PROJECT_ROOT_PATH = Path(__file__).parent

# Top level directories
BUILDERS_PATH = Path(PROJECT_ROOT_PATH / "builders")
DATA_PATH = Path(PROJECT_ROOT_PATH / "data")
DOCS_PATH = Path(PROJECT_ROOT_PATH / "docs")
PACKAGE_PATH = Path(PROJECT_ROOT_PATH / "osrsbox")
SCRIPTS_PATH = Path(PROJECT_ROOT_PATH / "scripts")
TEST_PATH = Path(PROJECT_ROOT_PATH / "test")

# Useful data paths
DATA_CACHE_PATH = Path(DATA_PATH / "cache")
DATA_WIKI_PATH = Path(DATA_PATH / "wiki")
DATA_ICONS_PATH = Path(DATA_PATH / "icons")
DATA_ITEMS_PATH = Path(DATA_PATH / "items")
DATA_MONSTERS_PATH = Path(DATA_PATH / "monsters")
DATA_SCHEMAS_PATH = Path(DATA_PATH / "schemas")

# Useful builder paths
BUILDERS_ITEMS = Path(BUILDERS_PATH / "items")
BUILDERS_MONSTERS = Path(BUILDERS_PATH / "monsters")

# Useful scripts paths
SCRIPTS_ITEMS = Path(SCRIPTS_PATH / "items")
SCRIPTS_MONSTERS = Path(SCRIPTS_PATH / "monsters")
SCRIPTS_SCHEMAS = Path(SCRIPTS_PATH / "schemas")
SCRIPTS_UPDATE = Path(SCRIPTS_PATH / "update")

# User agent for wiki scraping requests
custom_agent = {
    'User-Agent': "osrsbox - @PH01L#7906",
    'From': "phoil@osrsbox.com"
}
