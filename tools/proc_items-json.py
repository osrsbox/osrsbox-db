import os
import glob
import json

fis = glob.glob("items-json" + os.sep + "*")

items_json = dict()

for fi in fis:
    with open(fi) as f:
        temp = json.load(f)
        items_json[temp["id"]] = temp

for k,v in items_json.items():
    # print(items_json[k]["quest_item"], items_json[k]["id"])
    # print(items_json[k]["release_date"], items_json[k]["id"])
    print(items_json[k]["examine"], items_json[k]["id"])