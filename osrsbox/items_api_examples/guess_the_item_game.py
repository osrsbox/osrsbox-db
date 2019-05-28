"""
Description:
A very simple 'game' that gets a random item's examine text from the osrsbox-db item database
and asks the user to guess the name of the item
"""


from osrsbox import items_api
import random

if __name__ == "__main__":
    all_db_items = items_api.load()
    item_found = False
    item_name = ""
    while item_found == False:
        random_id = random.randint(1,len(all_db_items))
        for item in all_db_items:
            # Discard items with examine text on None, this is not a required field.
            if item.examine != None and item.id == random_id:
                print(item.examine)
                item_found = True
                item_name = item.name

    answer = input("What is this item? ")

    if answer == item_name:
        print("Well done!")
    else:
        print(f"No, this was a {item_name}")
