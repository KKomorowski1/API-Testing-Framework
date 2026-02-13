# performance/locustfile.py
from locust import HttpUser, task, between
from services.booking_service import BookingService
from config.config import config
from utils.data_processor import DataProcessor

class BookingPerformanceUser(HttpUser):
    wait_time = between(1, 5)
    host = config.BASE_URL  # Uses the environment-specific URL from config.py

    def on_start(self):
        """
        Runs once per user. We can initialize our service here.
        Note: Locust's HttpUser.client is compatible with requests.
        """
        # We wrap our existing service around the Locust client
        self.booking_service = BookingService(self.host)
        self.booking_service.session = self.client 
        
        # Process test data using your existing DataProcessor
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