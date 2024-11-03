import pytest
import requests 
from requests.auth import HTTPBasicAuth

from config_provider import ConfigProvider


@pytest.fixture(scope="session")
def before_after_all():
    # Setup before all tests
    yield
    # Cleanup after all tests


@pytest.fixture
def context() -> dict:

    # Setup before each test
    context = { }
    context["book_ids"] = []
    yield context

    # Cleanup after each test (Delete any books added during this test)
    for book_id in context["book_ids"]:
        url = ConfigProvider.get_host() + "/books"
        headers = {
            'g-token': 'ROM831ESV',
            'Content-Type': 'application/json'
            }
        auth = HTTPBasicAuth(ConfigProvider.get_username(), ConfigProvider.get_password())
        requests.request("DELETE", url, headers=headers, auth=auth)
