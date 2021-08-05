"""
Author:  PH01L
Email:   phoil@osrsbox.com
Website: https://www.osrsbox.com

Description:
Convert items icons to base64 and populate icons-items-complete.json file.

Copyright (c) 2021, PH01L

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
import json
import base64
import hashlib
from pathlib import Path

import config


def get_md5(file_path):
    h = hashlib.new("md5")
    with open(file_path, "rb") as file:
        block = file.read(512)
        while block:
            h.update(block)
            block = file.read(512)

    return h.hexdigest()


def main():
    # Set path for item icon files and glob PNGs
    fis = Path(config.DOCS_PATH / "items-icons").glob("*")

    # Set output dictionary for JSON export
    all_icons = dict()

    # Sort icon files numerically
    item_ids = [x.stem for x in fis]
    item_ids = sorted(item_ids)

    # Loop all item IDs, and process each PNG
    for item_id in item_ids:
        # Set the image file location
        image_name = f"{item_id}" + ".png"
        image_path = Path(config.DOCS_PATH / "items-icons" / image_name)

        # Check for default images, and remove them
        md5 = get_md5(image_path)
        if md5 == "af7f8e0df9cce2bc800d1ae9f5372d99":
            image_path.unlink()
            continue

        # Open PNG file, and convert to Base64
        with open(image_path, "rb") as f:
            b64_data = base64.b64encode(f.read())
            b64_image = b64_data.decode()
            all_icons[item_id] = b64_image

    # Export all converted PNG images to a JSON file to docs folder
    out = Path(config.DATA_PATH / "icons" / "icons-items-complete.json")
    with open(out, "w") as f:
        json.dump(all_icons, f, indent=4)


if __name__ == "__main__":
    main()
