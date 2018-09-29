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
        if val[0] == "-":
            if val[1:].isdigit():
                return int(val)
        else:
            if val.isdigit():
                return int(val)

def _floatcast(val):
    """ Convert input to float. """
    if val is None:
        return None
    if isinstance(val, float):
        return val
    if isinstance(val, str):
        return float(val)                
                
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
# QuestDetails object
class QuestDetails(object):
    def __init__(self, wikicode):
        # Wikicode of the OSRS Wiki quest page
        self.wikicode = wikicode

    # Infobox quest
    @property
    def start(self):
        return self._start
    @start.setter
    def start(self, value):
        self._start = _strcast(value)

    @property
    def difficulty(self):
        return self._difficulty
    @difficulty.setter
    def difficulty(self, value):
        self._difficulty = _strcast(value)

    @property
    def description(self):
        return self._description
    @description.setter
    def description(self, value):
        self._description = _strcast(value)

    @property
    def requirements(self):
        return self._requirements
    @requirements.setter
    def requirements(self, value):
        self._requirements = _strcast(value)

    @property
    def items(self):
        return self._items
    @items.setter
    def items(self, value):
        self._items = _strcast(value)

    @property
    def reccomended(self):
        return self._reccomended
    @reccomended.setter
    def reccomended(self, value):
        self._reccomended = _strcast(value)

    @property
    def kills(self):
        return self._kills
    @kills.setter
    def kills(self, value):
        self._kills = _strcast(value)
