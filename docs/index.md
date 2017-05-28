---
layout: default
title: OSRSBox | osrsbox-db | An Old School Runescape (OSRS) Database of Items
---

# osrsbox-db
## An Old School Runescape (OSRS) RESTful API

This repository is a database of Old School Runescape (OSRS) items in JSON format with accomapnying icon images in PNG format. The repository provides public access to metadata about every OSRS item in the game; for example, whether an item is tradeable, stackable, or equipable or if the item is members only, or a quest item. For any equipable item, there is metadata about combat stats the item has; for example, what slash attack bonus, magic defence bonus or prayer bonus an item provides. Furthermore, high and low alchemy values are provided. Lastly, each item has a corresponding item icon in PNG format. 

## osrsbox-db: JSON structured data

The osrsbox-db stores information about OSRS items in separate JSON files. For example, [this link](https://osrsbox.github.io/osrsbox-db/items-json/1/12453.json "osrsbox.github.io/osrsbox-db/items-json/1/12453.json") provides direct access to the 12453.json file, which holds metadata about the Black wizard hat (g) item. In OSRS the id number 12453 is unique to the Black wizard hat (g). This is why the item id is utilised in the catalogue for fetching all item information. 

### Structure JSON data about OSRS items

But what is actually contained in these JSON files? Well, it is a collection of metadata (information) about the specific item. There are two main categories of metadata about an item: 1) item properties; and 2) item stats. All items have properties; for example, the item's weight and the items high alchemy value. All item properties are listed below for reference, including the data type (e.g., string, integer, float) for each property and a description of the property.

| Property        | Data type       | Description                                  |
|-----------------|-----------------|----------------------------------------------|
| id              | integer         | Unqiue OSRS item ID number                   |
| name            | string          | Name of the item                             |
| release_date    | string          | Date the item was released                   |
| members_only    | boolean integer | If the item is a members only item or not    |
| quest_item      | boolean integer | If the item is a quest item or not           |
| tradeable       | boolean integer | If the item is tradeable or not              |
| equipable       | boolean integer | If the item is equipable or not              |
| stackable       | boolean integer | If the item is stackable or not              |
| edible          | boolean integer | If the item is edible or not                 |
| store_price     | integer         | The store price of the item                  |
| high_alch       | integer         | The high alchemy value of the item           |
| low_alch        | integer         | The low alchemy value of the item            |
| buy_limit       | integer         | The Grand Exchange buy limit of the item     |
| weight          | float           | The weight (in kilograms) of the item        |
| destroy         | string          | How to destroy the item                      |
| examine         | string          | The examine text of the item                 |
| url             | string          | Wikia URL link                               |



If an item is equipable it will have additional metadata about the combat bonuses that it provides; for example, the melee strength bonus the Dragon dagger item provides. The following table specifies the 14 different stats an item may provide. Please note that all item stats are stored as an interger data type.

| Property        | Data type       | Description                                  |
|-----------------|-----------------|----------------------------------------------|
| attack_stab     | int             | The stab attack bonus of the item            |
| attack_slash    | int             | The slash attack bonus of the item           |
| attack_crush    | int             | The crush attack bonus of the item           |
| attack_magic    | int             | The magic attack bonus of the item           |
| attack_ranged   | int             | The ranged attack bonus of the item          |
| defence_stab    | int             | The stab defence bonus of the item           |
| defence_slash   | int             | The slash defence bonus of the item          |
| defence_crush   | int             | The crush defence bonus of the item          |
| defence_magic   | int             | The magic defence bonus of the item          |
| defence_ranged  | int             | The ranged defence bonus of the item         |
| melee_strength  | int             | The melee strength bonus of the item         |
| ranged_strength | int             | The ranged strength bonus of the item        |
| magic_damage    | int             | The magic damage bonus of the item           |
| prayer          | int             | The prayer bonus of the item                 |


So what does this JSON object actually look like? Well, listed below is an example of a complete JSON object for the Black wizard hat (g). Or you could just click on [this link](https://osrsbox.github.io/osrsbox-db/items-json/1/12453.json "Black wizard hat (g) in JSON format!") to view the raw JSON using the osrsbox-db API.

```json
{
   "id":12453,
   "name":"Black wizard hat (g)",
   "release_date":"12 June 2014",
   "members_only":0,
   "quest_item":0,
   "tradeable":1,
   "equipable":1,
   "stackable":0,
   "edible":0,
   "store_price":0,
   "high_alch":1,
   "low_alch":0,
   "buy_limit":0,
   "weight":0.4,
   "destroy":"Drop",
   "examine":"A silly pointed hat, with colourful trim.",
   "url":"http://2007.runescape.wikia.com/wiki/Black_wizard_hat_(g)",
   "attack_stab":0,
   "attack_slash":0,
   "attack_crush":0,
   "attack_magic":2,
   "attack_ranged":0,
   "defence_stab":0,
   "defence_slash":0,
   "defence_crush":0,
   "defence_magic":2,
   "defence_ranged":0,
   "melee_strength":0,
   "ranged_strength":0,
   "magic_damage":0,
   "prayer":0
}

```

### Accessing JSON data about OSRS items

The JSON file for each OSRS item can be directly accessed using unqiue URLs provide through the osrsbox.github.io website. Technically, this provides the functionality of a RESTful API, but only supports GET requests. That is, you can fetch JSON files using a unique URL but cannot modify any JSON content. Below is a list of URL examples for items in the osrsbox-db:

+ <https://osrsbox.github.io/osrsbox-db/items-json/1/12453.json>
+ <https://osrsbox.github.io/osrsbox-db/items-json/1/10.json>
+ <https://osrsbox.github.io/osrsbox-db/items-json/2/2003.json>
+ <https://osrsbox.github.io/osrsbox-db/items-json/3/3097.json>
+ <https://osrsbox.github.io/osrsbox-db/items-json/3/3098.json>

As displayed by the links above, each item ID is stored in the "osrsbox-db" repository, under the "items-json" folder. This folder has ten subdirectories named from 0 to 9. Each of these folders stores JSON objects based on the first digit in the item ID. Subfolders are essential to use, as storing more than 5,000 JSON files in one folder in a GitHub repository is both messy, and takes a very long time to browse using the GitHub wesbite.

So how can you get these JSON files about OSRS items? It is pretty easy, but really depends on what you are trying to accomplish and what programming language you are using. Take a simple example of downloading a single JSON file. In a Linux system, we could simply use the wget command to download a single JSON file, as illustrated in the example code below:

```bash
wget https://osrsbox.github.io/osrsbox-db/items-json/1/12453.json
```

Maybe you are interested in downloading a single (or potentially multiple) JSON files about OSRS items and processing the information in a Python program. The short script below downloads the 12453.json file using Python's urllib library, loads the data as a JSON object and prints the contents to the console. The code is a little messy, primarily due to supporting both Python 2 and 3 (as you can see from the "try" and "except" importing method implemented).

```python
import json

try:
    from urllib.request import urlopen
except ImportError:
    from urllib2 import urlopen

url = ("https://osrsbox.github.io/osrsbox-db/items-json/1/12453.json")
response = urlopen(url)
data = response.read().decode("utf-8")
json_obj = json.loads(data)
print(data)
```

Finally, let's have a look at Javascript (specifically jQuery) example to fetch a JSON file from the osrsbox-db and build an HTML element to display in a webpage. The example below is a very simple method to download the JSON file using the jQuery getJSON function. Once we get the JSON file, we loop through the JSON entries and print each key and value (e.g., "name" and "Black wizard hat (g)") on it's own line in a div element. If you want to experiment with the code, the code is available in a W3Schools TryIt Editor at [this link](https://www.w3schools.com/code/tryit.asp?filename=FDYXVMBAV85L "Working Javascript / jQuery example of osrsbox-db").

```html
<!DOCTYPE html>
<html>
  <head>
    <script src="https://ajax.googleapis.com/ajax/libs/jquery/3.1.1/jquery.min.js"></script>
    <script>
      $(document).ready(function(){
          $("button").click(function(){
              $.getJSON("https://osrsbox.github.io/osrsbox-db/items-json/1/12453.json", function(result){
                  $.each(result, function(i, field){
                      $("div").append(i + " " + field + "<br>");
                  });
              });
          });
      });
    </script>
  </head>
  <body>
    <button>Get JSON data</button>
    <div></div>
  </body>
</html>
```

### Using JSON data about OSRS items

So, if you have read this far, we can fetch OSRS item information using a public API provided by osrsbox-db... But what can we do with this data? This section covers some examples of usage to display how the information in each JSON file can be useful. However, the primary reason the osrsbox-db was written was to enable osrsbox-tooltips!

Treasure trails example from web page

Tooltips page using the JSON api

Python example

## osrsbox-db: Icon images in PNG format

![alt text](https://osrsbox.github.io/osrsbox-db/items-icons/1/12453.png "Black wizard hat (g)")

<span id="forkongithub"><a href="https://github.com/osrsbox/osrsbox-db">Fork me on GitHub</a></span>

