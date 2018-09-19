# !/usr/bin/python

"""
Author:  PH01L
Email:   phoil@osrsbox.com
Website: osrsbox.com
Date:    2018/09/01

Description:
Extract the buy limit from OSRS Wiki Items pages

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

import requests
import urllib.request
import lxml.html
import lxml.etree
import json

def extract_buy_limit(itemName):
    url = "http://oldschoolrunescape.wikia.com/wiki/" + itemName
    #http://oldschoolrunescape.wikia.com/api.php?action=parse&prop=wikitext&format=json&page=
    print("URL: %r" % url)

    data = urllib.request.urlopen(url).read()
    doc = lxml.html.fromstring(data)

    # Try and fetch the Wikia infobox for the item
    box = doc.xpath("//table[@class='wikitable infobox']")
    if not box:
        # If not discovered, try another Wikia infobox class
        box = doc.xpath("//table[@class='wikitable infobox plainlinks']")
        if not box:
            # Only for furnature pages
            box = doc.xpath("//table[@class='wikitable infobox plainlinks [[:Template:Parentitle]]']")[0]
        else:
            box = box[0]
    else:
        box = box[0]
    buy_limit = None

    # Fetch all the tr elements and loop through them
    trs = box.xpath("tr")
    for tr in trs:                     
        # Find the title of each tr element
        tr_title = tr.xpath("th/a/text()")
        # print("tr_title:", tr_title)
        
        # Find corresponding value for property 
        value = tr.xpath("td/text()")
        # print("value:   ", value)
            
        try:
            propertyTitle = tr_title[0]
        except IndexError:
            continue
        
        # Find the buy limit
        propertyTitle = propertyTitle.strip()
        propertyTitle = propertyTitle.lower()
        propertyTitle = propertyTitle.replace(" ", "")
        # print(propertyTitle)
        if propertyTitle == "buylimit":
            try:
                buy_limit = tr.xpath("td/text()")[0]
                buy_limit = buy_limit.strip()
                buy_limit = int(buy_limit)
            except (ValueError, IndexError):
                buy_limit = None

    return buy_limit

def query_category_items():
    for result in query_category_items_callback({'generator': 'categorymembers'}):
        # Process result data
        for r in result['pages']:
            page_suffix = result['pages'][r]["title"]
            page_suffix = page_suffix.replace(" ", "_")
            page_suffix = page_suffix.replace("'", "%27")
            buy_limit = extract_buy_limit(page_suffix)
            print("%s|%s" % (result['pages'][r]["title"], buy_limit))

def query_category_items_callback(request):
    request['action'] = 'query'
    request['format'] = 'json'
    request['prop'] = 'categories'
    request['gcmtitle'] = 'Category:Items'
    request['gcmlimit'] = 'max'
    request['cllimit'] = 'max'
    lastContinue = {}
    while True:
        # Clone original request
        req = request.copy()
        # Modify the original request
        # Insert values returned in the 'continue' section
        req.update(lastContinue)
        # Call API
        result = requests.get('http://oldschoolrunescape.wikia.com/api.php', params=req).json()
        # print(result)
        if 'error' in result:
            #raise Error(result['error'])
            print(">>> ERROR!")
            break
        if 'warnings' in result:
            print(result['warnings'])
        if 'query' in result:
            yield result['query']
        if 'query-continue' not in result:
            break
        if 'categorymembers' not in result['query-continue']:
            break
        lastContinue = result['query-continue']['categorymembers']

################################################################################
if __name__=="__main__":   
    print(">>> Print starting...")
    # Start processing    
    query_category_items()
