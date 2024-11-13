import grpc
from concurrent import futures
import booking_pb2
import booking_pb2_grpc
import json

class BookingService(booking_pb2_grpc.BookingService):

   def __init__(self):
      with open('{}/data/bookings.json'.format("."), "r") as jsf:
         self.db = json.load(jsf)["bookings"]

   def Home(self, request, context):
        print("Home")
        response = booking_pb2.HomeResponse()
        response.message = "<h1>Bienvenue sur booking</h1>"
        return response

   def GetAllBookings(self, request, context):
      print("GetAllBookings")
      response = booking_pb2.AllBookingsResponse()
      for booking in self.db:
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
      print(response)
      return response

   def GetBookingsForUser(self, request, context):
      print("GetBookingsForUser")
      response = booking_pb2.BookingsUserResponse()
      for booking in self.db:
         if booking["userid"] == request.userid:
               response.userid = booking["userid"]
               for date in booking["dates"]:
                  date_item = booking_pb2.DateItem(
                     date=date["date"],
                     movies=date["movies"]
                  )
                  response.dates.append(date_item)
               break
      return response

   def AddBookingForUser(self, request, context):
      new_booking = {
         "userid": request.userid,
         "date": request.date,
         "movies": [request.movieid]
      }

      # Rechercher l'utilisateur dans les données existantes
      user_found = False
      for booking in self.db:
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
         self.db.append({
               "userid": request.userid,
               "dates": [new_booking]
         })

      # Préparer la réponse
      response = booking_pb2.BookingsUserResponse(userid=request.userid)
      for booking in self.db:
         if booking["userid"] == request.userid:
               for date in booking["dates"]:
                  date_item = booking_pb2.DateItem(
                     date=date["date"],
                     movies=date["movies"]
                  )
                  response.dates.append(date_item)
               break
      return response

def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    booking_pb2_grpc.add_BookingServiceServicer_to_server(BookingService(), server)
    server.add_insecure_port('[::]:3003')
    server.start()
    server.wait_for_termination()

        
if __name__ == '__main__':
    serve()


