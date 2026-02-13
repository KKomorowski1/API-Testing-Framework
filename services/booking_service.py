from core.api_client import APIClient

class BookingService(APIClient):
    ENDPOINT = "booking"
    
    def get_bookings(self):
        return self.get(f"{self.ENDPOINT}")

    def create_booking(self, payload):
        return self.post(self.ENDPOINT, json=payload)

    def update_booking(self, booking_id, payload):
        return self.put(f"{self.ENDPOINT}/{booking_id}", json=payload)

    def delete_booking(self, booking_id):
        return self.delete(f"{self.ENDPOINT}/{booking_id}")
