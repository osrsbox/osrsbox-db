import pytest
from pathlib import Path


PATH_TO_TEST_DIR = Path(__file__).absolute().parent


@pytest.fixture(scope="session")
def path_to_docs_dir() -> Path:
    return PATH_TO_TEST_DIR / ".." / "docs"
