# osrsbox-db
## An Old School Runescape (OSRS) RESTful API

This repository is a database of Old School Runescape (OSRS) items in JSON format with accomapnying icon images in PNG format. The repository provides public access to metadata about every OSRS item in the game; for example, whether an item is tradeable, stackable, or equipable or if the item is members only, or a quest item. For any equipable item, there is metadata about combat stats the item has; for example, what slash attack bonus, magic defence bonus or prayer bonus an item provides. Furthermore, high and low alchemy values are provided. Lastly, each item has a corresponding item icon in PNG format. 

## osrsbox-db: JSON structured data

The osrsbox-db stores information about OSRS items in separate JSON files. For example, [this link](https://osrsbox.github.io/osrsbox-db/items-json/1/12453.json "osrsbox.github.io/osrsbox-db/items-json/1/12453.json") provides direct access to the 12453.json file, which holds metadata about the Black wizard hat (g) item. In OSRS item id number 12453 is unique to the Black wizard hat (g) item, this is why the item id is utilised in the database. The JSON file for each OSRS item can be directly accessed using unqiue URLs provide through the osrsbox.github.io website. 

### Accessing structure JSON data about OSRS items

Intro

List of URL examples

osrsbox-db/items-json/1/12453.json
                      1/10.json
osrsbox-db/items-json/2/2010.json
osrsbox-db/items-json/3/3199.json
                      3/3999.json

Examples of URLS

<https://osrsbox.github.io/osrsbox-db/items-json/1/12453.json>

Below is an example os a complete JSON object for the Black wizard hat (g)

```json
{
    "url":"http://2007.runescape.wikia.com/wiki/Black_wizard_hat_(g)",
    "id":12453,
    "caption":"Black wizard hat (g)",
    "release_date":"12 June 2014",
    "members_only":0,
    "quest_item":0,
    "tradeable":1,
    "equipable":1,
    "stackable":0,
    "high_alch":1,
    "low_alch":0,
    "destroy":"Drop",
    "store_price":0,
    "weight":0.4,
    "examine":"A silly pointed hat, with colourful trim.",
    "edible":0,
    "ge_price":0,
    "buy_limit":0,
    "attack_stab":"+0",
    "attack_slash":"+0",
    "attack_crush":"+0",
    "attack_magic":"+2",
    "attack_ranged":"+0",
    "defence_stab":"+0",
    "defence_slash":"+0",
    "defence_crush":"+0",
    "defence_magic":"+2",
    "defence_ranged":"+0",
    "melee_strength":"+0",
    "ranged_strength":"0",
    "magic_damage":"0%",
    "prayer":"+0"
}
```

## osrsbox-db: Icon images in PNG format

![alt text](https://osrsbox.github.io/osrsbox-db/items-icons/1/12453.png "Black wizard hat (g)")
