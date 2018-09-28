import os
import glob
import json

################################################################################
if __name__=="__main__":
    import argparse
    ap = argparse.ArgumentParser()
    ap.add_argument("-d", 
                    "--dir", 
                    required=True,
                    help="Location of local directory of items-json (usually ../docs/items-json/")
    ap.add_argument("-k", 
                    "--key", 
                    required=False,
                    help="Select a key from the JSON API to print (e.g., name)")
    args = vars(ap.parse_args())

    dir = args["dir"]
    key = args["key"]

    # print(">>> Processing directory: %s" % dir)
    # print(">>> Printing following key: %s" % key)

    fis = glob.glob(dir + os.sep + "*")
    for fi in fis:
        with open(fi) as f:
            json_obj = json.load(f)
            print("%s" % str(json_obj[key]))
