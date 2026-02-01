import pytest
from config.config import config  # Import the instance
from services.auth_service import AuthService
from services.booking_service import BookingService

@pytest.fixture(scope="session")
def auth_token():
    auth = AuthService(config.BASE_URL)
    return auth.login(config.USERNAME, config.PASSWORD)

@pytest.fixture(scope="function")
def booking_service(auth_token):
    service = BookingService(config.BASE_URL)
    service.set_auth_cookie(auth_token)
    return service