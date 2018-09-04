import os
import urllib.request
import json
import collections
import string
import time
import requests

# if not os.path.exists("icons"):
#     os.makedirs("icons")
# else:
#     print("Folder named 'icons' already exists. Exiting.")
#     quit()

# Generate a list of lowercase letters, a-z
alpha = string.ascii_lowercase

# Specify all split URLs to later built URL to fetch
# Final result of a URL is provided below:
# api/catalogue/items.json?category=1&alpha=a&page=1
base_url = "http://services.runescape.com/m=itemdb_oldschool/"
category_url = "api/catalogue/items.json?category="
alpha_url = "&alpha="
page_url = "&page="

# Specify URL components (used to iterate)
category = 1
# alpha_req = 0
# page_req = 1
alpha_req = 1
page_req = 7

# Build initial URL
url = (base_url + 
       category_url + 
       str(category) + 
       alpha_url + 
       alpha[alpha_req] + 
       page_url + 
       str(page_req))
       
total = 0
done = 0

page = urllib.request.urlopen(url).read().decode("utf-8")
page = json.loads(page)
total = int(page['total'])

while done <= total:
    url = (base_url + 
           category_url + 
           str(category) + 
           alpha_url + 
           alpha[alpha_req] + 
           page_url + 
           str(page_req))
           
    print(url)           
    
    page = requests.get(url).json()
    done += 12
    
    # Process each item in the list
    for item in page['items']:
        icon = item["icon"] 
        fn = "icons/" + icon.split('=')[-1] + ".gif"
        urllib.request.urlretrieve(icon,fn)
        #icon_large = item["icon_large"] 
        #fn = "icons_large/" + icon_large.split('=')[-1] + ".gif"
        #urllib.request.urlretrieve(icon_large,fn)
        
    # Handle next page
    if len(page['items']) < 12:
        # Increase alpha counter for next letter
        alpha_req += 1
        # Reset page counter to 1, for new letter
        page_req = 1
    else:
        # Increase category page interator
        page_req += 1
    time.sleep(12)

"""
When done:
mogrify -format png icons/*.gif
mv icons/*.png icons-png
"""