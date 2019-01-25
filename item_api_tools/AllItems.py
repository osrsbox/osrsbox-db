# !/usr/bin/python

"""
Author:  PH01L
Email:   phoil@osrsbox.com
Website: osrsbox.com
Date:    2018/12/18

Description:
AllItems is a class to handle multiple osrsbox-db item-json files or a
single items_complete.json file.

Copyright (c) 2018, PH01L

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

>>> CHANGELOG:
    0.1.0       Base functionality
"""

__version__ = "0.1.0"

import os
import json
import glob
import logging

from . import ItemDefinition

log = logging.getLogger(__name__)


class AllItems:
    def __init__(self, input_data_file_or_directory):
        self.all_items = []  # TODO: Check to see which of these are necessary
        self.all_items_dict = {}  # TODO: Check to see which of these are necessary
        self.load_all_items(input_data_file_or_directory)

    def __iter__(self):
        for item_id in self.all_items:
            yield item_id

    def get_itemids_objects(self):
        # Return keys
        return self.all_items_dict.items()

    def get_itemids(self):
        # Return keys
        return self.all_items_dict.keys()

    def get_objects(self):
        # Return values
        return self.all_items_dict.values()

    def load_all_items(self, input_data_file_or_directory):
        # Handle input_data (either items-json dir, or items_complete.json)
        if os.path.isdir(input_data_file_or_directory):
            if input_data_file_or_directory.endswith("/"):
                path = input_data_file_or_directory + "*"
            else:
                path = os.path.join(input_data_file_or_directory, "*")

            self._load_items_from_directory(path_to_directory=path)

        elif os.path.isfile(input_data_file_or_directory):
            self._load_items_from_file(input_data_file_or_directory)

    def _load_items_from_directory(self, path_to_directory: str):
        """
        The directory should contain json file objects with items.

        The `items-json` directory contains the format for these files.
        """
        count = 1
        # Loop through every item file
        for json_file in glob.glob(path_to_directory):

            if os.path.isdir(json_file):
                continue

            log.debug("Processing item: %d" % count)
            with open(json_file) as f:
                temp = json.load(f)

            self._load_item(temp)
            count += 1

    def _load_items_from_file(self, path_to_json_file: str):
        """The `path_to_json_file` should be a json file containing a structure like `all_items.json`."""
        count = 1

        with open(path_to_json_file) as f:
            temp = json.load(f)

        for entry in temp:
            self._load_item(temp[entry])
            count += 1

    def _load_item(self, item_json):
        """Convert the ``item_json`` into a :class:`ItemDefinition.ItemDefinition` and store it."""
        # Load the item using the ItemDefinition class
        item_definition = ItemDefinition.ItemDefinition()
        item = item_definition.load_item(item_json)

        # Add item to list and dict
        self.all_items.append(item)
        self.all_items_dict[item.id] = item
