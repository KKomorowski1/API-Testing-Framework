from pydantic import BaseModel
from typing import Optional

class BookingDates(BaseModel):
    checkin: str
    checkout: str

class BookingDetails(BaseModel):
    firstname: str
    lastname: str
    totalprice: int | str 
    depositpaid: bool
    bookingdates: BookingDates
    additionalneeds: Optional[str] = None

class BookingResponse(BaseModel):
    bookingid: int
    booking: BookingDetails