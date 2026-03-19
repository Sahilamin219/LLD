"""Requirements:
1. System supports three vehicle types: Motorcycle, Car, Large Vehicle
2. When a vehicle enters, system automatically assigns an available compatible spot
3. System issues a ticket at entry.
4. When a vehicle exits, user provides ticket ID
   - System validates the ticket
   - Calculates fee based on time spent (hourly, rounded up)
   - Frees the spot for next use
5. Pricing is hourly with same rate for all vehicles
6. System rejects entry if no compatible spot is available
7. System rejects exit if ticket is invalid or already used

Out of scope:
- Payment processing
- Physical gate hardware
- Security cameras or monitoring
- UI/display systems
- Reservations or pre-booking"""

# Entities:
# Vechile - id, type( motor, car, large )
# Ticket - entry time, exit time, Ticketid, price
# ParkingSpot - id, type, 
#              Ticket - entry time, exit time, Ticketid, price
#              states : empty, occupied(vehicleID)

# Orchastrator:
# ParkingLot:
#      ParkingSpotList
#     +GetAvailableSpot(vechileType)
#     +ProcessExit(ticketId) - calculates fees and releases spot



# Flow/Behavouir - 
# user -> entry -> ParkingLot -> Reserve/Reject -> ParkingSpot
# user -> exit -> ProcessExit(ParkingSpot) -> Ticket
from enum import Enum
from uuid import uuid4
import datetime
import math
import threading
class VehicleType(Enum):
    MOTOR = "MOTOR"
    CAR = "CAR"
    LARGE = "LARGE"
class Rate(Enum):
    MOTOR = 10
    CAR = 50
    LARGE = 100
class Ticket:
    def __init__(self, entryTime: datetime.datetime, vehicleType: VehicleType):
        self.entryTime = entryTime
        self.exitTime = None
        self.ticketID = uuid4()
        self.vehicleType = vehicleType
        self.price = 0

    def assignPrice(self):
        self.exitTime = datetime.datetime.now()
        duration = self.exitTime - self.entryTime
        hours = math.ceil(duration.total_seconds() / 3600)
        self.price = hours * Rate[self.vehicleType.name].value

class ParkingSpot:
    parkingNumber = 0
    def __init__(self, type):
        self.occupied = False
        self.parkingID = ParkingSpot.parkingNumber
        ParkingSpot.parkingNumber += 1
        self.ticket = None
        self.type = type
class ParkingSpotAllocationStrategy:
    pass
class ParkingLot:
    def __init__(self):
        self.active_tickets = {}
        self.parkingSpotList = {}
        self._lock = threading.Lock()
        self.parkingSpotList[VehicleType.MOTOR] = [ ParkingSpot(VehicleType.MOTOR) for i in range(10) ]
        self.parkingSpotList[VehicleType.CAR] = [ ParkingSpot(VehicleType.CAR) for i in range(10) ]
        self.parkingSpotList[VehicleType.LARGE] = [ ParkingSpot(VehicleType.LARGE) for i in range(10) ]

    
    def getAvailableSpot(self, vehicleType):
        # Lock ensures two concurrent callers can't allocate the same spot.
        with self._lock:
            for spot in self.parkingSpotList[vehicleType]:
                if not spot.occupied:
                    spot.occupied = True
                    spot.ticket = Ticket(datetime.datetime.now(), vehicleType)
                    self.active_tickets[str(spot.ticket.ticketID)] = spot
                    return spot.ticket.ticketID
            raise Exception("No spot available")
    
    def ProcessExit(self, ticketID):
        # Lock keeps spot + ticket state consistent under concurrency.
        with self._lock:
            key = str(ticketID)
            if key not in self.active_tickets:
                raise Exception("Invalid ticket")
            spot = self.active_tickets.pop(key, None)
            if spot is None:
                raise Exception("Invalid ticket")
            spot.ticket.assignPrice()
            spot.occupied = False
            return spot.ticket
    