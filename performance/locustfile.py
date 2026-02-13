from locust import HttpUser, task, between
import sys
import os

# Add root directory to path so we can import from config/utils
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from config.config import config
from utils.data_processor import DataProcessor

class BookingUser(HttpUser):
    # Simulate a user waiting 1-3 seconds between tasks
    wait_time = between(1, 3)
    
    # We set the host from our Config class (Dynamic Environment!)
    host = config.BASE_URL

    def on_start(self):
        """
        Runs once when a User starts. We log in here.
        """
        response = self.client.post("/auth", json={
            "username": config.USERNAME,
            "password": config.PASSWORD
        })
        
        if response.status_code == 200:
            self.token = response.json().get("token")
            # Update headers for subsequent requests
            self.client.headers.update({"Cookie": f"token={self.token}"})
        else:
            print(f"Login Failed! Status: {response.status_code}")

    @task(1)
    def get_booking_ids(self):
        """
        Lightweight task: Get list of bookings.
        """
        self.client.get("/booking", name="/booking (List IDs)")

    @task(2)
    def create_dynamic_booking(self):
        """
        Heavy task: Create a booking using our shared JSON data + Dynamic Dates.
        """
        # 1. Load shared data template
        # We reuse the logic that calculates {{today}} automatically
        payloads = DataProcessor.load_and_process_json("booking_valid.json")
        
        # Pick the first scenario from the file
        payload = payloads[0]

        # 2. Send Request
        with self.client.post("/booking", json=payload, catch_response=True, name="/booking (Create)") as response:
            if response.status_code == 200:
                response.success()
                
                # Optional: Delete it immediately to keep DB clean during load test
                # booking_id = response.json().get("bookingid")
                # self.client.delete(f"/booking/{booking_id}")
            else:
                response.failure(f"Failed to create booking: {response.status_code}")