# !/usr/bin/python

"""
Author:  PH01L
Email:   phoil@osrsbox.com
Website: osrsbox.com
Date:    2017/11/28

Description:
HERE
Copyright (c) 2017, PH01L

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
import collections

import urllib.request
import lxml.html
import lxml.etree
import collections

import time
import glob
import datetime

months = [
"January",
"February",
"March",
"April",
"May",
"June",
"July",
"August",
"September",
"October",
"November",
"December"
]

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
    if val == "":
        return 0
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
    elif val in ["True", "true", "Yes", "yes", True]:
        return True
    elif val in ["False", "false", "No", "no", False]:
        return False
        
def _datecast(val):
    """ Check date by converting to datetime object, and convert back to str. """
    if val is None:
        return None
    try:
        date = datetime.datetime.strptime(val, "%d %B %Y")   
        return date.strftime("%d %B %Y")
    except:
        print("  > %s" % val)
        val = input("  > Enter a correct date: ")
        return _datecast(val)

###############################################################################
# ScrapeItemFromWikia object
class ScrapeItemFromWikia(object):
    def __init__(self, item_name, verbose):
        self.all_items = dict()
        self.verbose = verbose
        self.item_name = item_name
        self.weapon_slot = None
        self.weapon_speed = None
        self.url = None
        self.properties = dict()
        self.previous_property = ""
        self.bonuses = {"attack_stab" : None,
                        "attack_slash" : None,
                        "attack_crush" : None,
                        "attack_magic" : None,
                        "attack_ranged" : None,
                        "defence_stab" : None,
                        "defence_slash" : None,
                        "defence_crush" : None,
                        "defence_magic" : None,
                        "defence_ranged" : None,
                        "melee_strength" : None,
                        "ranged_strength" : None,
                        "magic_damage" : None,
                        "prayer" : None}
        
    def get_all_item_urls(self):
        print(">>> Fetching all item URLS from http://oldschoolrunescape.wikia.com")
		
        # Fetch the first items page from the OSRS Wikia
        data = urllib.request.urlopen('http://2007.runescape.wikia.com/wiki/Category:Items').read() 

        # Parse the fetched html document using lxml
        doc = lxml.html.fromstring(data)

        # Parse the list of items at bottom of item page
        uls = doc.xpath("//div[@class='mw-content-ltr']/table/tr/td")
           
        # Print what page we are processing
        print("  > Processed page 1")       
           
        # Initialise storage for fetched items
        alln = list()
           
        # Parse the ul elements
        for ul in uls:
            items = ul.xpath("//td/ul/li/a")
            for item in items:
                alln.append(item)

        # Further process ul elements
        for item in alln:
            #print(lxml.etree.tostring(item))
            item_name = item.xpath("text()")[0]
            base_url = "http://2007.runescape.wikia.com"
            item_url = base_url + item.xpath("@href")[0]
            self.all_items[item_name] = item_url   
           
        # Loop over every additional page (there are 28 currently)
        i = 2
        while i <= 30: 
            # NOTE: The above number (30) needs to be MANAUALLY CHANGED 
            # when the number of items on the Wikia site increases and
            # makes more pages
            url = 'http://2007.runescape.wikia.com/wiki/Category:Items?page=' + str(i)
            data = urllib.request.urlopen(url).read()
            doc = lxml.html.fromstring(data)
            uls1 = doc.xpath("//div[@class='mw-content-ltr']/table/tr/td")
            
            print("  > Processed page %d" % i)  
            
            alln = list()
            for ul in uls1:
                items = ul.xpath("//td/ul/li/a")
                for item in items:
                    alln.append(item)
            
            for item in alln:
                #print(lxml.etree.tostring(item))
                item_name = item.xpath("text()")[0]
                base_url = "http://2007.runescape.wikia.com"
                item_url = base_url + item.xpath("@href")[0]
                self.all_items[item_name] = item_url
            i = i + 1   
                              
    def save_all_item_urls(self):
        """ Output item names and Wikia URLs to CSV file named 'all_wikia_items'. """
        with open("all_wikia_items.csv", "w") as f:
            for item_name, item_url in self.all_items.items():
                f.write("%s,%s\n" % (item_name, item_url))
        f.close()
        
    def read_all_item_urls(self):
        """ Reload item names and Wikia URLs from CSV file named 'all_wikia_items'. """
        with open("all_wikia_items.csv") as f:
            for line in f:
                # print("%r" % line)
                line = line.strip()
                item_name, item_url = line.split(",")
                self.all_items[item_name] = item_url
        f.close()       
        
    def determine_item_url(self):
        name = self.item_name
        name = name.lower()
                
        # Clean name, especially for potions, black mask, enchanted rings etc.
        name = name.replace("(1)", "")
        name = name.replace("(2)", "")
        name = name.replace("(3)", "")
        name = name.replace("(4)", "")
        name = name.replace("(5)", "")
        name = name.replace("(6)", "")
        name = name.replace("(7)", "")
        name = name.replace("(8)", "")
        name = name.replace("(9)", "")
        name = name.replace("(10)", "")

        # Fix for broken items
        name = name.replace("(broken)", "")

        # Clean name for trimmed amulets etc
        # name = name.replace("(t1)", "")
        # name = name.replace("(t2)", "")
        # name = name.replace("(t3)", "")
        # name = name.replace("(t4)", "")
        # name = name.replace("(t5)", "")
        # name = name.replace("(t6)", "")        

        # Clean name for imbued black mask
        # name = name.replace("(1) ", "")
        # name = name.replace("(2) ", "")
        # name = name.replace("(3) ", "")
        # name = name.replace("(4) ", "")
        # name = name.replace("(5) ", "")
        # name = name.replace("(6) ", "")
        # name = name.replace("(7) ", "")
        # name = name.replace("(8) ", "")
        # name = name.replace("(9) ", "")
        # name = name.replace("(10) ", "")        
        
        # Skill cape trimmed cleaner
        # name = name.replace("(t)", "")

        # Empty cleaner
        name = name.replace("(empty)", "")
        
        # Crystal normalisers
        name = name.replace("1/10", "")
        name = name.replace("2/10", "")
        name = name.replace("3/10", "")
        name = name.replace("4/10", "")
        name = name.replace("5/10", "")
        name = name.replace("6/10", "")
        name = name.replace("7/10", "")
        name = name.replace("8/10", "")
        name = name.replace("9/10", "")
        name = name.replace("(10)", "")

        # Crystal imbued normalisers
        # name = name.replace("1/10 (i)", "")
        # name = name.replace("2/10 (i)", "")
        # name = name.replace("3/10 (i)", "")
        # name = name.replace("4/10 (i)", "")
        # name = name.replace("5/10 (i)", "")
        # name = name.replace("6/10 (i)", "")
        # name = name.replace("7/10 (i)", "")
        # name = name.replace("8/10 (i)", "")
        # name = name.replace("9/10 (i)", "")
        # name = name.replace("(10) (i)", "")        
        # name = name.replace("full (i)", "") 
        # name = name.strip()

        # Poison replacers       
        name = name.replace("(p)", "")        
        name = name.replace("(p+)", "")
        name = name.replace("(p++)", "")

        # Eyes of glourphrie quest items
        # if name.startswith("a "):
        #     name = name[2:]
        # if name.startswith("an "):
        #     name = name[3:]

        # Full normaliser, never seems to have a different page
        name = name.replace("(full)", "")

        # Black jack fixes
        # name = name.replace("(o)", " (o)")
        # name = name.replace("(d)", " (d)")

        # Fungicide spray
        # name = name.replace(" 10", "")
        # name = name.replace(" 9", "")
        # name = name.replace(" 8", "")
        # name = name.replace(" 7", "")
        # name = name.replace(" 6", "")
        # name = name.replace(" 5", "")
        # name = name.replace(" 4", "")
        # name = name.replace(" 3", "")
        # name = name.replace(" 2", "")
        # name = name.replace(" 1", "")
        # name = name.replace(" 0", "")

        # pharaohs scepter
        # name = name.replace(" (1)", "")
        # name = name.replace(" (2)", "")
        # name = name.replace(" (3)", "")
        # name = name.replace(" (4)", "")
        # name = name.replace(" (5)", "")
        # name = name.replace(" (6)", "")
        # name = name.replace(" (7)", "")
        # name = name.replace(" (8)", "")
        # name = name.replace(" (9)", "")
        # name = name.replace(" (10)", "")        

        # Random fixer
        name = name.replace("(kp)", "")

        # Nightmare Zone items
        name = name.replace("(nz)", "")

        # Barrows normalisers
        # name = name.replace(" 100", "")
        # name = name.replace(" 75", "")
        # name = name.replace(" 50", "")
        # name = name.replace(" 25", "")
        # name = name.replace(" 0", "")

        # Mysterious emblem fixes
        name = name.replace(" (tier 2)", "")
        name = name.replace(" (tier 3)", "")
        name = name.replace(" (tier 4)", "")
        name = name.replace(" (tier 5)", "")
        name = name.replace(" (tier 6)", "")
        name = name.replace(" (tier 7)", "")
        name = name.replace(" (tier 8)", "")
        name = name.replace(" (tier 9)", "")        
        name = name.replace(" (tier 10)", "")        

        # challenge scroll fixers
        if "challenge scroll (medium)" == name:
            name = "challenge scroll"
        if "challenge scroll (hard)" == name:
            name = "challenge scroll"
        if "challenge scroll (elite)" == name:
            name = "challenge scroll"    
        if "puzzle box (elite)" == name:
            name = "puzzle box"   
        if "puzzle box (hard)" == name:
            name = "puzzle box"                                     

        # More crystal equipment replacers
        if name.startswith("new "):
            name = name.replace("new ", "")

        name = name.strip()
        
        print("  > Searching for: %r" % name)        
        
        potential_matches = list()
        for item_name, item_url in self.all_items.items():
            if name in item_name.lower():
                potential_matches.append((item_name, item_url))
            # If an exact match, continue with it
            if name == item_name.lower():
                self.url = item_url
                print("  > Selected: %s" % item_name)
                print("  > WikiaURL: %s" % self.url)
                self.data = urllib.request.urlopen(self.url).read()
                return True, self.url
                   
        if len(potential_matches) > 1:
            potential_matches.sort()
            for i, item in enumerate(potential_matches):
                print('    {} {}'.format(i, item[0]))

            selection = input("  > Select the correct item from the list (url, or N): ")
            if selection.lower() == 'n':
                return False, None
            if selection == "url":
                self.url = input("  > Enter a URL: ")
                print("  > Selected: %s" % item_name)
                print("  > WikiaURL: %s" % self.url)
                self.data = urllib.request.urlopen(self.url).read()
                return True, self.url
            selection = int(selection)
            if selection not in range(0, len(potential_matches)):
                print(">>> ERROR: Selection is not in range.")
                self.determine_item_url()
            else:
                self.url = potential_matches[selection][1]
                print("  > Selected: %s" % (potential_matches[selection][0]))
                print("  > WikiaURL: %s" % self.url)
                self.data = urllib.request.urlopen(self.url).read()
                return True, self.url
        elif len(potential_matches) == 0:
            # Item not found, exiting
            print(">>> ERROR: Item not found")
            selection = input("  > Manually change the name (y, url, or N): ")
            if selection.lower() == 'y':
                name = input("  > Enter the new name: ")
                for item_name, item_url in self.all_items.items():
                    if name in item_name.lower():
                        self.url = self.all_items[item_name]
                        print("  > Selected: %s" % item_name)
                        print("  > WikiaURL: %s" % self.url)
                        self.data = urllib.request.urlopen(self.url).read()
                        return True, self.url
            if selection == "url":
                self.url = input("  > Enter a URL: ")
                print("  > Selected: %s" % item_name)
                print("  > WikiaURL: %s" % self.url)
                self.data = urllib.request.urlopen(self.url).read()
                return True, self.url
            return False, None
        else:
            self.url = potential_matches[0][1]
            print("  > Selected: %s" % (potential_matches[0][0]))
            print("  > WikiaURL: %s" % self.url)
            self.data = urllib.request.urlopen(self.url).read()
            return True, self.url

    def fix_bonus_value(self, value):
        value = value.strip()
        if " " in value:
            value = value.split(" ")[2]
            return value
        else:
            return value

    def get_item_bonuses(self):
        print("  > Fetching item bonuses...")
        # Parse the fetched html document using lxml
        if not hasattr(self, 'data'):
            print(">>> Error: Table not found for equipable item")
            answer = input("  > Would you like to set a ZERO table? [y, N]: ")
            if answer.lower() == "y":
                for key, value in self.bonuses.items():
                    self.bonuses[key] = 0
                self.item_slot = input("  > What slot is this item: ")
                self.weapon_speed = input("  > What speed is this item: ")
                return self.bonuses, self.item_slot, self.weapon_speed
        
        doc = lxml.html.fromstring(self.data)
           
        try:
            table = doc.xpath("//table[@class='wikitable smallpadding']")[0]
        except IndexError:
            table = None
            print(">>> Error: Table not found for equipable item")
            answer = input("  > Would you like to set a ZERO table? [y, N]: ")
            if answer.lower() == "y":
                for key, value in self.bonuses.items():
                    self.bonuses[key] = 0
                self.item_slot = input("  > What slot is this item: ")
                self.weapon_speed = input("  > What speed is this item: ")
            
            return self.bonuses, self.item_slot, self.weapon_speed 
            
        # If a Wikia info box has been extracted, process it
        if table is not None:
            # Fetch all the tr elements in the info box
            trs = table.xpath("tr")
                     
            # Need 3,6,9 for item bonuses
            # Need 8 for item slot
            # Need 10 for attack speed
            for i, tr in enumerate(trs):        
                if i == 3:
                    # Attack tr element
                    tds = tr.xpath("td/text()")
                    self.bonuses["attack_stab"] = self.fix_bonus_value(tds[0])
                    self.bonuses["attack_slash"] = self.fix_bonus_value(tds[1])
                    self.bonuses["attack_crush"] = self.fix_bonus_value(tds[2])
                    self.bonuses["attack_magic"] = self.fix_bonus_value(tds[3])
                    self.bonuses["attack_ranged"] = self.fix_bonus_value(tds[4])
                elif i == 6:
                    # Defense tr element
                    tds = tr.xpath("td/text()")
                    self.bonuses["defence_stab"] = self.fix_bonus_value(tds[0])
                    self.bonuses["defence_slash"] = self.fix_bonus_value(tds[1])
                    self.bonuses["defence_crush"] = self.fix_bonus_value(tds[2])
                    self.bonuses["defence_magic"] = self.fix_bonus_value(tds[3])
                    self.bonuses["defence_ranged"] = self.fix_bonus_value(tds[4])
                elif i == 9:
                    # Strength tr element
                    tds = tr.xpath("td/text()")
                    self.bonuses["melee_strength"] = self.fix_bonus_value(tds[0])
                    self.bonuses["ranged_strength"] = self.fix_bonus_value(tds[1])
                    self.bonuses["magic_damage"] = self.fix_bonus_value(tds[2])
                    if " " in tds[3]:
                        prayer = tds[3].split(" ")
                        if "(t)" in self.item_name:
                            self.bonuses["prayer"] = "+4"
                        else:
                            self.bonuses["prayer"] = prayer[0]
                    else:
                        self.bonuses["prayer"] = tds[3].strip()
                elif i == 8:
                    ths = tr.xpath("th/p/a/@title")
                    if len(ths) == 0:
                        self.item_slot = input("  > What slot of this item: ")
                    else:
                        item_slot = ths[0]
                        self.item_slot = item_slot.replace(" slot", "").lower()
                elif i == 10:
                    ths = tr.xpath("th/span/img/@alt")
                    # if ths:
                    if len(ths) == 0:
                        self.weapon_speed = input("  > What speed is this item: ")
                    else:
                        self.weapon_speed = ths[0]
                        self.weapon_speed = self.weapon_speed.split(" ")
                        self.weapon_speed = self.weapon_speed[len(self.weapon_speed) - 1]
                    # else:
                        # pass
                                        
            # Loop through bonuses and fix "+" and "%" and int cast value
            for bonus_name, bonus_value in self.bonuses.items():
                bonus_value = bonus_value.replace("+", "")
                bonus_value = bonus_value.replace("%", "")
                self.bonuses[bonus_name] = _intcast(bonus_value)
            print(self.bonuses)
            return self.bonuses, self.item_slot, self.weapon_speed
        
    def clean_string(self, value):
        """ Clean a string extracted from the Wikia infobox. """
        # First, strip the string
        value = value.strip()
        return value
            
    def clean_weight(self, weight):
        """ Clean the weight property extracted from a Wikia infobox. """
        # First, strip the string
        weight = weight.strip()
        # Remove a less than or greater than sign
        weight = weight.replace("<", "")
        weight = weight.replace(">", "")
        weight = weight.replace("~", "")
        # Replace "\xa0" - a space
        weight = weight.replace("\xa0", "")
        # Replace kg, all weights should be in kg
        weight = weight.replace("kg", "")
        weight = weight.replace("Unknown", "0")
        weight = weight.replace("Whole: ", "")
        weight = weight.replace("(empty) ", "")
        # Floatcast the string 
        if "to" in weight:
            print("  > weight:", weight)
            weight = input("  > Enter weight? [float]:")
        try:
            weight = float(weight)
        except:
            print("  > weight:", weight)
            weight = input("  > Enter weight? [float]:")
        weight = _floatcast(weight)
        return weight
        
    def clean_boolean(self, boolean):
        """ Clean boolean values extracted from a Wikia infobox. """
        # First, strip the string
        boolean = boolean.strip()
        # Cast the value
        boolean = _boolcast(boolean)
        return boolean    

    def clean_examine(self, examine):
        """ Clean boolean values extracted from a Wikia infobox. """
        # First, strip the string
        examine = examine.strip()
        return examine         

    def clean_quest(self, quest):
        """ Clean boolean values extracted from a Wikia infobox. """
        # First, strip the string
        quest = quest.strip()
        # Check there is a quest name
        if quest is not "":
            # Cast the value
            quest = _boolcast(True)
        else:
            quest = _boolcast(False)
            
        return quest           
        
    def clean_int(self, int):
        """ Clean the date property extracted from a Wikia infobox. """
        # First, strip the string
        int = int.strip()
        # Replace "\xa0" - a space
        int = int.replace("\xa0", "")
        # Replace kg, all weights should be in kg
        int = int.replace("coins", "")
        int = int.replace("Coins", "")
        # Replace any thousand separation commas
        int = int.replace(",", "")
        # Incast the string 
        int = _intcast(int)
        return int        
        
    def clean_release_date(self, date):
        """ Clean boolean values extracted from a Wikia infobox. """
        # First, strip the string
        date = date.strip()
        # Remove the word update
        date = date.replace(" Update", "")
        date = date.replace(",", "")
        # Cast the value
        date = _datecast(date)
        return date           
        
    
        
    def get_item_properties(self):
        
        print("  > Fetching item properties...")

        # Parse the fetched html document using lxml
        doc = lxml.html.fromstring(self.data)

        # Try and fetch the Wikia infobox for the item
        box = doc.xpath("//table[@class='wikitable infobox']")
        if not box:
            # If not discovered, try another Wikia infobox class
            box = doc.xpath("//table[@class='wikitable infobox plainlinks']")
            if not box:
                # Only for furnature pages
                box = doc.xpath("//table[@class='wikitable infobox plainlinks [[:Template:Parentitle]]']")[0]
                #return False
                # Should print error then return
            else:
                box = box[0]
        else:
            box = box[0]
        
        # Start scraping data from the infobox
        caption = box.xpath("caption/text()")[0].strip()
        if caption == "":
            caption = box.xpath("caption/b/text()")[0]
            self.properties["members_only"] = "1"
            self.properties["equipable"] = "0"
            self.properties["stackable"] = "1"
            self.properties["destroy"] = "Drop"
            self.properties["weight"] = "0"
        self.properties["caption"] = caption

        # Variable for the previously processed tr element
        previous_tr = ""
        
        # Fetch all the tr elements and loop through them
        trs = box.xpath("tr")
        for tr in trs:                     
            # If tr is an image, skip it
            if tr.xpath("td/a/@href"):
                if ".png" in tr.xpath("td/a/@href")[0]:
                    continue
                    
            # Find the title of each tr element
            tr_title = tr.xpath("th/a/text()")
            if not tr_title:
                # Get release date property
                tr_title = tr.xpath("th/text()")
                if tr_title:
                    tr_title = tr_title[0].strip()
                    tr_title = tr_title.lower()
                    tr_title = tr_title.replace(" ","_")
                # Or manually set title to examine (if it was last processed)
                elif self.previous_property == "examine":
                    tr_title = "examine2"
            else:
                tr_title = tr_title[0]
                tr_title = tr_title.lower()
                tr_title = tr_title.replace(" ","_")

            # Skip a couple of un-needed properties
            if tr_title == "exchange_price":
                continue
            if tr_title == "destroy":
                continue                 
            
            if self.verbose:
                print(tr_title)
            
            # Find corresponding value for property 
            value = tr.xpath("td/text()")
              
            # Set examine text
            if tr_title == "examine2":
                self.properties["examine"] = value  
                print(value)
              
            # Additional checks and fixes
            if tr_title == "buy_limit" and value[0] == " ":
                value = tr.xpath("td/i/text()")
                if value[0] == "Unknown" or value[0] == "unknown":
                    value[0] = "-1"
                      
            # Quest item work around
            if tr_title == "quest_item":
                temp_value = value[0].strip()
                if temp_value == 'No' or temp_value == 'Yes':
                    value = tr.xpath("td/text()")
                else:
                    temp_value = tr.xpath("td/a/text()")
                    if len(temp_value) == 0:
                        value = value
                    else:
                        value = temp_value
                        
            # # Examine for furnature
            # if tr_title == "examine_text":
                # value = 
            
            # Weight item work-around
            # Only extract inventory weight
            if tr_title == "weight" and value[0] == " ":
                temp_value = tr.xpath("td/b/text()")
                if "inventory" in temp_value[0].lower():
                    # : 0.4\xa0
                    value[0] = value[1]
                    value[0] = value[0].replace(":", "")
                    value[0] = value[0].replace("\xa0", "")
            if tr_title == "weight" and "-" in value[0]:
                value[0] = value[0].strip()
                value[0] = value[0].replace("\xa0kg", "")
                temp_value = value[0].split("-")
                temp_value = str((float(temp_value[1]) + float(temp_value[0]))/2)
                value[0] = temp_value
                
            # Months are tricky, handle and parse the value
            # TODO: This code is rediculous and needs a tidy
            if tr_title == "release_date":
                parsing = False
                for month in months:
                    for v in value:
                        if month in v:
                            if tr.xpath("td/a/text()"):
                                n_value = tr.xpath("td/a/text()")[0]
                                parsing = True
                if not value:
                    value = None
                else:
                    value = value[0].strip()
                    if " (" in value:
                        value = value.split(" (")[0]
                
                if parsing:
                    value = value + " " + n_value
                
            if self.verbose:
                print(value)
                
            # Clean various values
            if tr_title == "weight":
                value = self.clean_weight(value[0])
            elif (tr_title == "stackable" or 
                  tr_title == "tradeable" or 
                  tr_title == "equipable" or 
                  tr_title == "members_only"):
                value = self.clean_boolean(value[0])
            elif (tr_title == "low_alch" or 
                  tr_title == "high_alch" or 
                  tr_title == "store_price" or 
                  tr_title == "buy_limit"):
                value = self.clean_int(value[0])
            elif tr_title == "release_date":
                value = self.clean_release_date(value)
            elif tr_title == "quest_item":
                value = self.clean_quest(value[0])
            elif tr_title == "examine2" or tr_title == "examine_text":
                print("HERE")
                value = self.clean_examine(value[0])
            
            # Append the property name and property value to the list of properties
            if tr_title == "examine_text":
                self.properties["examine2"] = value
            elif tr_title and value:
                self.properties[tr_title] = value
            elif tr_title and value == False:
                self.properties[tr_title] = value                
            
            # Save the current tr title for the next iteration
            if type(tr_title) == list:
                self.previous_property = ""
            else:
                self.previous_property = tr_title.lower()   
        
        # Loop of extraction has completed.
        # Can set defaults here
        try:
            value = self.properties["buy_limit"]
        except KeyError:
            self.properties["buy_limit"] = -1       
            
        return self.properties
            
################################################################################
if __name__=="__main__":
    # Run unit tests
    assert _intcast(-1) == -1
    assert _intcast("-1") == -1
  
    assert _boolcast("false") == False
    assert _boolcast("True")
    assert _boolcast("true")
    assert _boolcast(False) == False
    assert _boolcast(True)

    assert _strcast(1)
    assert _strcast("Hello world!")
    
    print("\nModule tests passed.\n")
