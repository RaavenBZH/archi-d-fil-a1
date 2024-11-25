import grpc
from concurrent import futures
import booking_pb2
import booking_pb2_grpc
import json
import os
import sys
sys.path.append(os.path.join(os.path.dirname(__file__), 'showtime'))
from showtime import showtime_pb2, showtime_pb2_grpc

# Constants
BOOKINGS_FILE = './data/bookings.json'
SHOWTIME_CHANNEL = 'showtime:3202'
PORT = 3201

class BookingService(booking_pb2_grpc.BookingServiceServicer):

    def __init__(self):
        with open(BOOKINGS_FILE, "r") as jsf:
            self.db = json.load(jsf)
        self.showtime_channel = grpc.insecure_channel(SHOWTIME_CHANNEL)
        self.showtime_stub = showtime_pb2_grpc.ShowtimeStub(self.showtime_channel)

    def write(self, bookings):
        """Helper function to write bookings to JSON file."""
        with open(BOOKINGS_FILE, 'w') as f:
            json.dump({"bookings": bookings}, f)

    def Home(self, request, context):
        """Home route to welcome users."""
        print("Home")
        response = booking_pb2.BookingHomeResponse()
        response.message = "<h1>Bienvenue sur booking</h1>"
        return response

    def GetAllBookings(self, request, context):
        """Route to get all bookings."""
        print("GetAllBookings")
        response = booking_pb2.AllBookingsResponse()
        for booking in self.db["bookings"]:
            booking_user = booking_pb2.BookingsUser(
                userid=booking["userid"],
                dates=[
                    booking_pb2.DateItem(
                        date=date["date"],
                        movies=date["movies"]
                    ) for date in booking["dates"]
                ]
            )
            response.bookings.append(booking_user)
        if len(response.bookings) <= 0:
            context.set_code(grpc.StatusCode.NOT_FOUND)
            context.set_details("No booking!")
        return response

    def GetBookingsForUser(self, request, context):
        """Route to get bookings for a specific user."""
        print("GetBookingsForUser")
        response = booking_pb2.BookingsUserResponse()
        responseFound = False
        for booking in self.db["bookings"]:
            if booking["userid"] == request.userid:
                response.userid = booking["userid"]
                for date in booking["dates"]:
                    date_item = booking_pb2.DateItem(
                        date=date["date"],
                        movies=date["movies"]
                    )
                    response.dates.append(date_item)
                responseFound = True
                break
        if not responseFound:
            context.set_code(grpc.StatusCode.NOT_FOUND)
            context.set_details("Booking not found for this user")
        else:
            context.set_code(grpc.StatusCode.OK)
            context.set_details("")
        return response

    def AddBookingForUser(self, request, context):
        """Route to add a booking for a specific user."""
        print("AddBookingForUser")

        showtime_request = showtime_pb2.Date(date=request.date)
        schedule = self.showtime_stub.GetSchedule(showtime_request)

        if request.movieid not in schedule.movies:
            context.set_code(grpc.StatusCode.INVALID_ARGUMENT)
            context.set_details("Film not scheduled on the specified date.")
            return booking_pb2.BookingsUserResponse()

        user_request = booking_pb2.UserIdRequest(userid=request.userid)
        response = self.GetBookingsForUser(user_request, context)
        for i in range(len(response.dates)):
            if response.userid == request.userid and response.dates[i].date == request.date and request.movieid in response.dates[i].movies:
                context.set_code(grpc.StatusCode.NOT_FOUND)
                context.set_details("Booking already exists!")
                return booking_pb2.BookingsUserResponse()

        new_booking = {
            "date": request.date,
            "movies": [request.movieid]
        }

        # Rechercher l'utilisateur dans les données existantes
        user_found = False
        for booking in self.db["bookings"]:
            if booking["userid"] == request.userid:
                # Ajouter la date ou mettre à jour les films pour cette date
                for date in booking["dates"]:
                    if date["date"] == request.date:
                        date["movies"].append(request.movieid)
                        break
                else:
                    # Si la date n'existe pas encore, l'ajouter
                    booking["dates"].append(new_booking)
                user_found = True
                break

        # Si l'utilisateur n'a pas été trouvé, créer une nouvelle réservation
        if not user_found:
            self.db["bookings"].append({
                "userid": request.userid,
                "dates": [new_booking]
            })

        self.write(self.db)

        # Préparer la réponse
        return self.GetBookingsForUser(user_request, context)

def serve():
    """Function to start the gRPC server."""
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    booking_pb2_grpc.add_BookingServiceServicer_to_server(BookingService(), server)
    server.add_insecure_port('[::]:3201')
    server.start()
    server.wait_for_termination()

if __name__ == '__main__':
    serve()