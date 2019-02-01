from pathlib import Path
import os

from osrsbox_db.item_api_tools.AllItems import AllItems

NUMBER_OF_ITEMS = 21409  # The current number of items being loaded from the db


def test_AllItems_load(path_to_docs_dir: Path):
    path_to_items_json_dir_no_slash = path_to_docs_dir / "items-json"
    path_to_items_json_dir_slash = os.path.join(path_to_docs_dir, "items-json", "")
    path_to_items_complete = path_to_docs_dir / "items_complete.json"

    for path in (path_to_items_json_dir_slash, path_to_items_json_dir_no_slash, path_to_items_complete):
        all_items = AllItems(str(path))
        assert len(all_items.all_items) == NUMBER_OF_ITEMS
        assert len(all_items.all_items_dict) == NUMBER_OF_ITEMS
