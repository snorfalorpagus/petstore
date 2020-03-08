import pytest
import sys
from pathlib import Path


sys.path.append(str(Path(__file__).parent.parent))

from app import create_app  # noqa: E402


@pytest.fixture
def test_client(loop, aiohttp_client):
    app = create_app()
    client = aiohttp_client(app.app)
    return loop.run_until_complete(client)
