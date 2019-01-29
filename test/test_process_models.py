from model_db_tools.ProcessModels import main

import json
from unittest.mock import MagicMock, patch, mock_open

import pytest


# @TODO(PH01L): We should get a version of this that uses live data instead of mocks.
@pytest.mark.parametrize("json_loads_return", [
    {"id": "id", "name": "name", "type": "items", "inventoryModel": ["model"]},
    {"id": "id", "name": "name", "type": "items", "models": ["model"]},
    {"id": "id", "name": "name", "type": "items", "objectModels": ["model"]},
])
@patch("model_db_tools.ProcessModels.os.path.basename", return_value="base_path")
@patch("model_db_tools.ProcessModels.glob.glob", side_effect=[[MagicMock()], [MagicMock()], [MagicMock()]])
def test_process_models(glob, basename, json_loads_return):
    with patch("model_db_tools.ProcessModels.open", mock_open(read_data=json.dumps(json_loads_return))):
        models_dict = main("mocked_path")
        assert len(models_dict) == 1
