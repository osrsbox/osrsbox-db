import urllib.request
import lxml.html
import lxml.etree

url = "http://oldschoolrunescape.wikia.com/wiki/Granite_maul"

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

print("Buy limit:", buy_limit)
