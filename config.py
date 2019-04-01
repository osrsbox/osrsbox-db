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

from pathlib import Path

PROJECT_ROOT_PATH = Path(__file__).parent

DATA_PATH = Path(PROJECT_ROOT_PATH / "data")
DOCS_PATH = Path(PROJECT_ROOT_PATH / "docs")
EXTRACTION_WIKI_PATH = Path(PROJECT_ROOT_PATH / "extraction_tools_wiki")
EXTRACTION_CACHE_PATH = Path(PROJECT_ROOT_PATH / "extraction_tools_cache")
ITEMS_BUILDER_PATH = Path(PROJECT_ROOT_PATH / "items_builder")
PACKAGE_ROOT_PATH = Path(PROJECT_ROOT_PATH / "osrsbox")
