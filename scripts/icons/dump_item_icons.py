"""
Author:  PH01L
Email:   phoil@osrsbox.com
Website: https://www.osrsbox.com

Description:
Dump item inventory icons using the RuneLite HTTP API.

Copyright (c) 2020, PH01L

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
from pathlib import Path
from concurrent.futures import as_completed
from concurrent.futures import ThreadPoolExecutor

import config
import requests


custom_agent = {
    'User-Agent': "osrsbox-agent",
    'From': "phoil@osrsbox.com"
}


def determine_runelite_api_version() -> str:
    """Fetch RuneLite HTTP API main page, and determine current API version."""
    # Set the base URL of the RuneLite API documentation page
    base_url = "https://static.runelite.net/api/http-service/"

    # Perform HTTP GET request
    try:
        page_data = requests.get(base_url,
                                 headers=custom_agent)
    except requests.exceptions.RequestException as e:
        raise SystemExit(">>> ERROR: Get request error. Exiting.") from e

    # Find RuneLite HTTP API base URL
    for line in page_data.text.split("\n"):
        if "HTTPS" in line:
            api_url = line.lower()
            return api_url


def download_png_image(url: str):
    """Download a item icon from RuneLite HTTP API URL.

    :param url: The full API URL of the PNG image.
    """
    try:
        page_data = requests.get(url,
                                 headers=custom_agent,
                                 stream=True)
    except requests.exceptions.RequestException as e:
        raise SystemExit(">>> ERROR: Get request error. Exiting.") from e

    return page_data.content


def extract_item_icons(api_url: str):
    """Extract all item icons using the RuneLite HTTP API.

    Example URL is:
    http://api.runelite.net/runelite-1.6.6.1/cache/item/998/image

    param api_url: The base RuneLite HTTP API URL.
    """
    base_url = api_url + "/cache/item/"
    all_urls = list()

    # Load the raw OSRS cache item data
    all_item_cache_data_path = Path(config.DATA_ITEMS_PATH / "items-cache-data.json")
    with open(all_item_cache_data_path) as f:
        all_item_cache_data = json.load(f)

    # Generate a list of URLs
    for item_id in all_item_cache_data:
        # Toogle for specific item ID numbers
        # item_id_int = int(item_id)
        # if item_id_int < 20000:
        #     continue

        query_url = f"{base_url}{item_id}/image"
        all_urls.append(query_url)

    with ThreadPoolExecutor(max_workers=None) as executor:
        future_to_url = {executor.submit(download_png_image, url): url for url in all_urls}
        for future in as_completed(future_to_url):
            # Get image data from function
            img_data = future.result()

            # Get url, extract item ID number, and set file path
            url = future_to_url[future]
            img_id = url.split("/")[-2]
            image_name = f"{img_id}.png"
            image_path = Path(config.DOCS_PATH / "items-icons" / image_name)

            # Save image
            with open(image_path, "wb") as f:
                f.write(img_data)
                print(f"  > Saved: {image_name}")


def main():
    """Program main entry point."""
    api_url = determine_runelite_api_version()
    extract_item_icons(api_url)


if __name__ == "__main__":
    main()
