import os
import sys
import json
import glob
import collections

sys.path.append(os.getcwd())
import OSRSItems

################################################################################
if __name__=="__main__":
    import argparse
    parser = argparse.ArgumentParser(description='''
Description.''')
    parser.add_argument("input",
                        help = "Directory with all Rulelite JSON files")
    parser.add_argument("output",
                        help = "Directory with fixed JSON files")                
    args = parser.parse_args()
    
    print(">>> Input directory: %s" % os.path.abspath(args.input))
		
    osrs_items = OSRSItems.OSRSItems(args.input, args.output)
    osrs_items.process_dir()
    # osrs_items.create_better_json()
    # osrs_items.output_item_list()

    
    # count = 0 
    # for item in osrs_items:
        # if item.equipable:
            # count += 1
            # # print(item.name)
    # print(count)