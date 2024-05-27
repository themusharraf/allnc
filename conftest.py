import pytest
from allnc.app import AllNc


@pytest.fixture
def app():
    return AllNc()


@pytest.fixture
def test_client(app):
    return app.test_session()
