import pytest
from app import AllNc


@pytest.fixture
def app():
    return AllNc()


@pytest.fixture
def test_client(app):
    return app.test_session()
