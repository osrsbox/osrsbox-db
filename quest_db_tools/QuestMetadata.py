# !/usr/bin/python

"""
Author:  PH01L
Email:   phoil@osrsbox.com
Website: osrsbox.com
Date:    2018/09/25

Description:


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
    1.0.0       Base functionality
"""

__version__ = "1.0.0"

import os
import sys
import json
import datetime
import collections
import logging
import re

# Pip install required
import requests
import mwparserfromhell
import dateparser

###############################################################################
# Helper methods
def _strcast(val):
    """ Convert value to string. """
    if val is None:
        return None
    return str(val)

def _intcast(val):
    """ Convert input to integer. """
    if val is None:
        return None
    if isinstance(val, int):
        return val
    if isinstance(val, str):
        return int(val)          
                
def _boolcast(val):
    """ Convert value to boolean object. """
    if val is None:
        return None
    elif val in ["True", "true", True, "Yes", "yes"]:
        return True
    elif val in ["False", "false", False, "No", "no"]:
        return False   

def _datecast(val):
    """ Check date by converting to datetime object, and convert back to str. """
    if val is None:
        return None
    elif isinstance(val, datetime.date):
        return val.strftime("%d %B %Y")
    date = datetime.datetime.strptime(val, "%d %B %Y")   
    return date.strftime("%d %B %Y")        

def _listcast(val):
    """ Check and convert to a list. """
    if val is None:
        return None
    elif isinstance(val, list):
        return val
    elif isinstance(val, str):
        temp_list = list()
        return temp_list.append(val)

###############################################################################
# QuestMetadata object
class QuestMetadata(object):
    def __init__(self, wikicode):
        # Wikicode of the OSRS Wiki quest page
        self.wikicode = wikicode

    # Infobox quest
    @property
    def number(self):
        return self._number
    @number.setter
    def number(self, value):
        self._number = _intcast(value)

    @property
    def members(self):
        return self._members
    @members.setter
    def members(self, value):
        self._members = _boolcast(value)

    @property
    def release_date(self):
        return self._release_date
    @release_date.setter
    def release_date(self, value):
        self._release_date = _datecast(value)	

    @property
    def series(self):
        return self._series
    @series.setter
    def series(self, value):
        self._series = _strcast(value)

    @property
    def difficulty(self):
        return self._difficulty
    @difficulty.setter
    def difficulty(self, value):
        self._difficulty = _strcast(value)

    @property
    def developer(self):
        return self._developer
    @developer.setter
    def developer(self, value):
        self._developer = _strcast(value)

    def wikicode_cleaner(self, input):
        clean_input = str(input)
        clean_input = clean_input.strip()
        clean_input = clean_input.replace("[", "")
        clean_input = clean_input.replace("]", "")
        return clean_input

    def populate(self):
        # print(self.wikicode)

        # Quest number
        try:
            number = self.wikicode.get("number").value
            self.number = self.wikicode_cleaner(number)
        except ValueError:
            self.number = None

        # Members or F2P
        try:
            members = self.wikicode.get("members").value
            self.members = self.wikicode_cleaner(members)
        except ValueError:
            self.members = None

        # Quest release date
        try:
            release = self.wikicode.get("release").value
            self.release = self.wikicode_cleaner(release)
        except ValueError:
            self.release = None   

        # Quest difficulty
        try:
            series = self.wikicode.get("series").value
            self.series = self.wikicode_cleaner(series)
        except ValueError:
            self.series = None

        # Quest difficulty
        try:
            difficulty = self.wikicode.get("difficulty").value
            self.difficulty = self.wikicode_cleaner(difficulty)
        except ValueError:
            self.difficulty = None

        # Quest developer
        try:
            developer = self.wikicode.get("developer").value
            self.developer = self.wikicode_cleaner(developer)
        except ValueError:
            self.developer = None

    ###########################################################################
    # Handle item to JSON
    def construct_json(self):
        self.json_out = collections.OrderedDict()
        self.json_out["number"] = self.number
        self.json_out["members"] = self.members
        self.json_out["release"] = self.release
        self.json_out["series"] = self.series
        self.json_out["difficulty"] = self.difficulty
        self.json_out["developer"] = self.developer
        return self.json_out
             