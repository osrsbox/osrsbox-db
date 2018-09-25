import collections

buylimits = dict()

with open("extract_buy_limits.txt") as f:
    for l in f:
        if "URL" in l or "None" in l or ">" in l:
            continue
        l = l.strip()
        l = l.split("|")
        buylimits[l[0]] = l[1]
        
with open("extract_buy_limits_EXISTING.txt") as f:
    for l in f:
        l = l.strip()
        l = l.split("|")
        buylimits[l[1]] = l[2]

with open("buy_limits.txt") as f:
    for l in f:
        l = l.strip()
        l = l.split("|")
        buylimits[l[0]] = l[1]

od = collections.OrderedDict()
for k,v in buylimits.items():
    od[k] = v

for k,v in od.items():
    v = v.replace(",", "")
    print("%s|%s" % (k,v))