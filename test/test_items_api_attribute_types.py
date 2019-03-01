"""
Author:  PH01L
Email:   phoil@osrsbox.com
Website: https://www.osrsbox.com

Description:
Tests for module: osrsbox.items_api.all_items

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

from osrsbox import items_api

ALL_DB_ITEMS = items_api.load()


@pytest.mark.parametrize("attribute,expected_type", [
    ("id", int),
    ("name", str),
    ("members", bool),
    ("tradeable", bool),
    ("tradeable_on_ge", bool),
    ("stackable", bool),
    ("noted", bool),
    ("noteable", bool),
    ("linked_id", bool),
    ("equipable", bool),
    ("cost", int),
    ("lowalch", int),
    ("highalch", int),
    ("weight", float),
    ("buy_limit", int),
    ("quest_item", bool),
    ("release_date", str),
    ("examine", str),
    ("url", str)
])
def test_items_api_attribute_type(attribute, expected_type):
    for item in ALL_DB_ITEMS:
        item_attr_value = getattr(item, attribute)
        if item_attr_value is None:
            continue
        assert isinstance(item_attr_value, expected_type)
