import os
import json

with open("extract_all_items_page_wikitext_bu.json") as f:
    all = json.load(f)

print("LENGTH OF ALL:", len(all))

with open("extract_all_items_page_wikitext2.json") as f:
    temp2 = json.load(f)

print("LENGTH OF TEMP2:", len(temp2))

for entry in temp2:
    if entry not in all:
        all[entry] = temp2[entry]
        #print("1 ADDED")

print("LENGTH OF ALL MODIFIED:", len(all))

fi_out = "extract_all_items_page_wikitext.json"
with open(fi_out, "w") as f:
    json.dump(all, f)

with open("extract_all_items_page_wikitext_bonuses_bu.json") as f:
    bonuses = json.load(f)

with open("extract_all_items_page_wikitext_bonuses2.json") as f:
    temp3 = json.load(f)

for entry in temp3:
    if entry not in bonuses:
        bonuses[entry] = temp3[entry]

fi_out = "extract_all_items_page_wikitext_bonuses.json"
with open(fi_out, "w") as f:
    json.dump(bonuses, f)