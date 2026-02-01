from core.api_client import APIClient

class AuthService(APIClient):
    def login(self, username, password):
        payload = {"username": username, "password": password}
        response = self.post("auth", json=payload)
        response.raise_for_status()
        return response.json().get("token")