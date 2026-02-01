import requests
import logging

class APIClient:
    def __init__(self, base_url):
        self.base_url = base_url
        self.session = requests.Session()
        self.session.headers.update({"Content-Type": "application/json"})
        self.logger = logging.getLogger(__name__)

    def set_auth_cookie(self, token):
        self.session.cookies.set("token", token)

    def _request(self, method, endpoint, **kwargs):
        url = f"{self.base_url}/{endpoint}"
        self.logger.info(f"REQ: {method} {url}")
        try:
            response = self.session.request(method, url, **kwargs)
            self.logger.info(f"RES: {response.status_code}")
            return response
        except requests.exceptions.RequestException as e:
            self.logger.error(f"Request failed: {e}")
            raise

    def get(self, endpoint, **kwargs): return self._request("GET", endpoint, **kwargs)
    def post(self, endpoint, **kwargs): return self._request("POST", endpoint, **kwargs)
    def put(self, endpoint, **kwargs): return self._request("PUT", endpoint, **kwargs)
    def delete(self, endpoint, **kwargs): return self._request("DELETE", endpoint, **kwargs)