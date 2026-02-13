# performance/locustfile.py
from locust import HttpUser, task, between
from services.auth_service import AuthService
from services.booking_service import BookingService
from config.config import config
from utils.data_processor import DataProcessor

class BookingPerformanceUser(HttpUser):
    wait_time = between(1, 5)
    host = config.BASE_URL  # Uses the environment-specific URL from config.py

    def on_start(self):
        """
        Runs once per user. Authenticate here to get a token.
        """
        # 1. Initialize services
        self.auth_service = AuthService(self.host)
        self.booking_service = BookingService(self.host)
        
        # 2. Sync the Locust client session with our services
        self.auth_service.session = self.client
        self.booking_service.session = self.client 
        
        # 3. Generate token and set auth cookie
        # Uses credentials from your .env file via config
        token = self.auth_service.login(config.USERNAME, config.PASSWORD)
        self.booking_service.set_auth_cookie(token)
        
        # 4. Process test data
        self.test_data = DataProcessor.load_and_process_json("booking_valid.json")[0]
        
    @task(3)
    def view_bookings(self):
        # Using existing service methods
        self.booking_service.get(self.booking_service.ENDPOINT)

    @task(1)
    def create_and_delete_booking(self):
        # Create a booking
        response = self.booking_service.create_booking(self.test_data)
        
        if response.status_code == 200:
            booking_id = response.json().get("bookingid")
            # Cleanup immediately to keep DB clean during load test
            self.booking_service.delete_booking(booking_id)