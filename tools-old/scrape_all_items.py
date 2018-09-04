import urllib.request
import lxml.html
import lxml.etree
import collections

############################################################################
def get_items():
    # Fetch the first items page from the OSRS Wikia
    data = urllib.request.urlopen('http://2007.runescape.wikia.com/wiki/Category:Items').read() 

    # Parse the fetched html document using lxml
    doc = lxml.html.fromstring(data)

    # Parse the list of items at bottom of item page
    uls = doc.xpath("//div[@class='mw-content-ltr']/table/tr/td")
       
    # Print what page we are processing
    print("PAGE 1")       
       
    # Initialise storage for fetched items
    all_items = dict()
    alln = list()
       
    # Parse the ul elements
    for ul in uls:
        npcs = ul.xpath("//td/ul/li/a")
        for npc in npcs:
            alln.append(npc)
    
    # Further process ul elements
    for npc in alln:
        #print(lxml.etree.tostring(npc))
        npc_name = npc.xpath("text()")[0]
        base_url = "http://2007.runescape.wikia.com"
        npc_link = base_url + npc.xpath("@href")[0]
        all_items[npc_name] = npc_link   
       
    # Loop over every additional page (there are 28 currently)
    i = 2
    while i < 31: # NOTE: This number (29) needs to be MANAUALL CHANGED 
        # For example, if more pages are added
        # It needs to be 1 more than the actual number of pages
        url = 'http://2007.runescape.wikia.com/wiki/Category:Items?page=' + str(i)
        data = urllib.request.urlopen(url).read()
        doc = lxml.html.fromstring(data)

        uls1 = doc.xpath("//div[@class='mw-content-ltr']/table/tr/td")
        
        print("PAGE", i)
        
        alln = list()
           
        for ul in uls1:
            npcs = ul.xpath("//td/ul/li/a")
            for npc in npcs:
                alln.append(npc)
        
        for npc in alln:
            #print(lxml.etree.tostring(npc))
            npc_name = npc.xpath("text()")[0]
            base_url = "http://2007.runescape.wikia.com"
            npc_link = base_url + npc.xpath("@href")[0]
            all_items[npc_name] = npc_link
        i = i + 1   
               
    # Now done processing all items
    
    # Print the length of items scraped   
    print(len(all_items))

    # Order the previously populated dictionary (a-z)
    od = collections.OrderedDict(sorted(all_items.items()))

    # Open file for writing all items to
    out_fi = open("all_wikia_items.txt", 'w')

    for k,v in od.items():
        #print(k + "\t" + v)
        out_fi.write(k + "\t" + v + "\n")

############################################################################
get_items()
