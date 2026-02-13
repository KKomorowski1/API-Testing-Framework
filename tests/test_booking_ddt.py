import pytest
from config.config import config  # Import the instance
from utils.data_processor import DataProcessor
from schemas.booking_schema import BookingResponse
from services.auth_service import AuthService
from services.booking_service import BookingService


valid_bookings = DataProcessor.load_and_process_json("booking_valid.json")

@pytest.fixture(scope="session")
def auth_token():
    auth = AuthService(config.BASE_URL)
    return auth.login(config.USERNAME, config.PASSWORD)

@pytest.fixture(scope="function")
def booking_service(auth_token):
    service = BookingService(config.BASE_URL)
    service.set_auth_cookie(auth_token)
    return service


@pytest.mark.parametrize("booking_data", valid_bookings)
def test_create_booking_success(booking_service, booking_data):
    # 1. Act: Call the service to create a booking
    response = booking_service.create_booking(booking_data)
    
    # 2. Assert: Status code should be 200
    assert response.status_code == 200
    
    # 3. Assert: Validate response structure using Pydantic schema
    BookingResponse(**response.json())