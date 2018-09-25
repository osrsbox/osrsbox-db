import glob
import json
import os

names = dict()

dir = "items"
print(">>> Processing dir: %s" % dir)
fis = glob.glob(dir + os.sep + "*")
total = len(fis)

for fi in fis:
    with open(fi) as f:
        json_obj = json.load(f)

        try:
            url = json_obj["url"]
        except KeyError:
            continue

        if url == None:
            continue
            
        url = url.replace("http://2007.runescape.wikia.com/wiki/", "")
        url = url.replace("http://oldschoolrunescape.wikia.com/wiki/", "")
        name = json_obj["name"]
        print("%s|%s" % (name, url))
