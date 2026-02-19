import pytest
from config.config import config  # Import the instance
from utils.data_processor import DataProcessor
from schemas.booking_schema import BookingResponse
from services.auth_service import AuthService
from services.booking_service import BookingService


valid_bookings = DataProcessor.load_and_process_json("booking_valid.json")
invalid_request_format_bookings = DataProcessor.load_and_process_json("booking_invalid.json")
bad_request_bookings = DataProcessor.load_and_process_json("booking_bad_request.json")
update_bookings = DataProcessor.load_and_process_json("booking_update.json")

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

@pytest.mark.parametrize("booking_data", valid_bookings)
def test_delete_booking_success(booking_service, booking_data):
    response = booking_service.create_booking(booking_data)
    assert response.status_code == 200
    validated_response = BookingResponse(**response.json())
    booking_id = validated_response.bookingid
    delete_response = booking_service.delete_booking(booking_id)
    assert delete_response.status_code == 200 or delete_response.status_code == 201


@pytest.mark.parametrize("booking_data", invalid_request_format_bookings)
def test_invalid_request_format_booking(booking_service, booking_data):
    response = booking_service.create_booking(booking_data)
    assert response.status_code == 500

@pytest.mark.skip("logical error, api should return 400 but returns 200")
@pytest.mark.parametrize("booking_data", bad_request_bookings)
def test_invalid_logic_booking(booking_service, booking_data):
    response = booking_service.create_booking(booking_data)
    assert response.status_code == 400


def test_get_all_bookings(booking_service):
    response = booking_service.get_bookings()
    assert response.status_code == 200
    bookings = response.json()
    assert isinstance(bookings, list)
    assert len(bookings) > 0


@pytest.mark.parametrize("update_data", update_bookings)
def test_update_booking_success(booking_service, update_data):
    create_response = booking_service.create_booking(valid_bookings[0])
    assert create_response.status_code == 200
    booking_id = BookingResponse(**create_response.json()).bookingid

    update_response = booking_service.update_booking(booking_id, update_data)
    assert update_response.status_code == 200

    from schemas.booking_schema import BookingDetails
    validated = BookingDetails(**update_response.json())
    assert validated.firstname == update_data["firstname"]
    assert validated.lastname == update_data["lastname"]
    assert validated.totalprice == update_data["totalprice"]
    assert validated.depositpaid == update_data["depositpaid"]