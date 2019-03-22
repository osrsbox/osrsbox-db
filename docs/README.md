## osrsbox-db: Public JSON API 

This folder contains the publicly available database/dataset and somewhat-RESTful API of osrsbox-db. Basically, every file inside this specific folder can be fetched using HTTP GET requests. The base URL for this folder is `https://www.osrsbox.com/osrsbox-db/`. Simply append any file name (from this folder) to the base URL, and you can fetch this data. You can also clone this entire repository and access the files provided in this folder, or download a single file for offline processing.
 
A summary of the files provided in the JSON API are listed below with descriptions:

- `items-icons`: Collection of PNG files (20K+) for every item inventory icon in OSRS.
- `items-json`: Collection of JSON files (20K+) of extensive item metadata for every item in OSRS.
- `items-json-slot`: Collection of JSON files extracted from the database that are specific for each equipment slot (e.g., head, legs).
- `prayer-icon`: Collection of PNG files for each prayer in OSRS.
- `prayer-json`: Collection of individual JSON files with properties and metadata about OSRS prayers.
- `items-complete.json`: A single JSON file that contains all single JSON files from `items-json`
- `items-summary.json`: A single JSON file that contains only the item name and item ID number.
- `models-summary.json`: A single JSON file that contains model ID numbers for items, objects, and NPCs.

## Accessing the JSON API

The JSON file for each OSRS item can be directly accessed using unique URLs provide through the `osrsbox.com` website. Technically, this provides some of the functionality of a RESTful API, but only supports GET requests. That is, you can fetch JSON files using a unique URL but cannot modify any JSON content. Below is a list of URL examples for items in the osrsbox-db:

- [https://www.osrsbox.com/osrsbox-db/items-json/12453.json](https://www.osrsbox.com/osrsbox-db/items-json/12453.json)
- [https://www.osrsbox.com/osrsbox-db/items-json/10.json](https://www.osrsbox.com/osrsbox-db/items-json/10.json)
- [https://www.osrsbox.com/osrsbox-db/items-json/2003.json](https://www.osrsbox.com/osrsbox-db/items-json/2003.json)
- [https://www.osrsbox.com/osrsbox-db/items-json/3097.json](https://www.osrsbox.com/osrsbox-db/items-json/3097.json)
- [https://www.osrsbox.com/osrsbox-db/items-json/3098.json](https://www.osrsbox.com/osrsbox-db/items-json/3098.json)

As displayed by the links above, each item ID is stored in the `osrsbox-db` repository, under the [`items-json`](https://github.com/osrsbox/osrsbox-db/tree/master/docs/items-json) folder. 

In addition to the single JSON files for each item, there is also a collection of JSON files that contain combined items. The following list documents the additional JSON files that are available:

- `items-complete.json`: A single JSON file containing every item. This file is also provided through the API and is available from [items-complete.json](https://www.osrsbox.com/osrsbox-db/items-complete.json)
- `items-json-slot`: A collection of JSON files that have the same database contents as `ītems-complete.json`, but are split into the different equipment slots. The following list documents all the files available:
    - [items-2h.json](https://www.osrsbox.com/osrsbox-db/items-json-slot/items-2h.json)
    - [items-ammo.json](https://www.osrsbox.com/osrsbox-db/items-json-slot/items-ammo.json)
    - [items-body.json](https://www.osrsbox.com/osrsbox-db/items-json-slot/items-body.json)
    - [items-cape.json](https://www.osrsbox.com/osrsbox-db/items-json-slot/items-cape.json)
    - [items-feet.json](https://www.osrsbox.com/osrsbox-db/items-json-slot/items-feet.json)
    - [items-hands.json](https://www.osrsbox.com/osrsbox-db/items-json-slot/items-hands.json)
    - [items-head.json](https://www.osrsbox.com/osrsbox-db/items-json-slot/items-head.json)
    - [items-legs.json](https://www.osrsbox.com/osrsbox-db/items-json-slot/items-legs.json)
    - [items-neck.json](https://www.osrsbox.com/osrsbox-db/items-json-slot/items-neck.json)
    - [items-ring.json](https://www.osrsbox.com/osrsbox-db/items-json-slot/items-ring.json)
    - [items-shield.json](https://www.osrsbox.com/osrsbox-db/items-json-slot/items-shield.json)
    - [items-weapon.json](https://www.osrsbox.com/osrsbox-db/items-json-slot/items-weapon.json)

So how can you get and use these JSON files about OSRS items? It is pretty easy but really depends on what you are trying to accomplish and what programming language you are using. 

### Accessing the JSON API using wget

Take a simple example of downloading a single JSON file. In a Linux system, we could use the `wget` command to download a single JSON file, as illustrated in the example code below:

```
wget https://www.osrsbox.com/osrsbox-db/items-json/12453.json
```

### Accessing the JSON API using Python

Maybe you are interested in downloading a single (or potentially multiple) JSON files about OSRS items and processing the information in a Python program. The short script below downloads the `12453.json` file using Python's urllib library, loads the data as a JSON object and prints the contents to the console. The code is a little messy, primarily due to supporting both Python 2 and 3 (as you can see from the "try" and "except" importing method implemented).

```
import json

try:
    from urllib.request import urlopen
except ImportError:
    from urllib2 import urlopen

url = ("https://www.osrsbox.com/osrsbox-db/items-json/12453.json")
response = urlopen(url)
data = response.read().decode("utf-8")
json_obj = json.loads(data)
print(data)
```

### Accessing the JSON API using JavaScript

Finally, let's have a look at JavaScript (specifically jQuery) example to fetch a JSON file from the osrsbox-db and build an HTML element to display in a web page. The example below is a very simple method to download the JSON file using the jQuery getJSON function. Once we get the JSON file, we loop through the JSON entries and print each key and value (e.g., name and Black wizard hat (g)) on its own line in a div element. If you want to experiment with the code, the code is available in a W3Schools TryIt Editor at [this link](https://www.w3schools.com/code/tryit.asp?filename=FY2CQ7W1J346).

```
<!DOCTYPE html>
<html>
  <head>
    <script src="https://ajax.googleapis.com/ajax/libs/jquery/3.1.1/jquery.min.js"></script>
    <script>
      $(document).ready(function(){
          $("button").click(function(){
              $.getJSON("https://www.osrsbox.com/osrsbox-db/items-json/12453.json", function(result){
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
