"""API Client for Inventoro."""

import logging
from datetime import datetime, timedelta

import backoff
import requests

logger = logging.getLogger(__name__)


def _ichunk(iterable, chunksize):
    """Chunk an iterable into chunks of size chunksize."""
    current = []
    for element in iterable:
        current.append(element)
        if len(current) == chunksize:
            yield current
            current = []
    if current:
        yield current


class APIClient:
    """API Client for Inventoro."""

    url = "https://api.inventoro.com/v1"

    def __init__(self, client_id, client_secret):
        self.client_id = client_id
        self.client_secret = client_secret
        self._session = requests.Session()
        self._access_token = None
        self._token_expiration = None

    @backoff.on_exception(backoff.expo, exception=(requests.HTTPError, requests.ConnectionError), max_time=60)
    def _get_token(self):
        """Post login credentials to get access token."""

        config = {
            "clientId": self.client_id,
            "secret": self.client_secret,
        }
        token_endpoint = f"{self.url}/login"
        response = self._session.post(token_endpoint, json=config)
        try:
            response.raise_for_status()
        except requests.HTTPError as error:
            if response.status_code == 429 or response.status_code >= 500:
                raise
            raise ValueError(f"Bad response status code - {response.status_code}") from error

        self._token_expiration = datetime.now() + timedelta(minutes=15)

        return response.json()["access_token"]

    @property
    def access_token(self):
        """Get access token."""

        if not self._access_token or (self._token_expiration and datetime.now() > self._token_expiration):
            self._access_token = self._get_token()

        return self._access_token

    @property
    def session(self):
        """Update header with a valid token."""

        self._session.headers.update({"Authorization": f"Bearer {self.access_token}"})

        return self._session

    def post_warehouse_products(self, data):
        """Post warehouse products to the API."""

        for chunk in _ichunk(data, 20):  # limit of 20 products per call
            response = self.session.put(f"{self.url}/import/warehouse-products", timeout=120, json=list(chunk))
            response.raise_for_status()

    def get_warehouse_products(self):
        """Get warehouse products from the API for validation of the result."""

        response = self.session.get(f"{self.url}/import/warehouse-products")
        response.raise_for_status()
        return response.json()
