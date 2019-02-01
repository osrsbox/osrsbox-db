"""
Author:  PH01L
Email:   phoil@osrsbox.com
Website: https://www.osrsbox.com

Description:
This script is a simple example to demonstrate how to access data in the
compressed definitions files provided in the osrsbox-db repository. This
example will load the compressed items.json file, and print the name
and members property to the console.

Copyright (c) 2019, PH01L

###############################################################################
This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.
This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.
You should have received a copy of the GNU General Public License
along with this program.  If not, see <http://www.gnu.org/licenses/>.
###############################################################################
"""

from extraction_tools_cache.osrs_cache_data import CacheDefinitionFiles


if __name__ == "__main__":
    # Set the file for the items.json file, which should be in the same directory as this script
    compressed_json_file = "items.json"

    # Initialize the CacheDefinitionFiles object, passing the items.json file as a parameter
    definitions = CacheDefinitionFiles(compressed_json_file)

    # Use the class generator to loop the definition file ID numbers in the object
    for id_number in definitions:
        print(f">>> Processing: {id_number}")
        # Use getitem to fetch information from the decompressed data using the ID number
        name_property = definitions[id_number]["name"]
        members_property = definitions[id_number]["members"]
        print(f"  > Item name: {name_property}")
        print(f"  > Item members status: {members_property}\n")
