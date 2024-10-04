# import grpc
# from concurrent import futures
# import booking_pb2
# import booking_pb2_grpc
import json

# class BookingServicer(booking_pb2_grpc.BookingServicer):

#     def __init__(self):
#         with open('{}/data/bookings.json'.format("."), "r") as jsf:
#             self.db = json.load(jsf)["schedule"]

# def serve():
#     server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
#     booking_pb2_grpc.add_BookingServicer_to_server(BookingServicer(), server)
#     server.add_insecure_port('[::]:3002')
#     server.start()
#     server.wait_for_termination()

#     with open('./databases/bookings.json'.format("."), "r") as jsf:

from flask import Flask, render_template, request, jsonify, make_response
import requests
import json
from werkzeug.exceptions import NotFound

app = Flask(__name__)

PORT = 3201
HOST = '0.0.0.0'

with open('./data/bookings.json'.format("."), "r") as jsf:
   bookings = json.load(jsf)["bookings"]

@app.route("/", methods=['GET'])
def home():
   return "<h1 style='color:blue'>Welcome to the Booking service!</h1>"

@app.route("/bookings", methods=['GET'])
def get_json():
    res = make_response(jsonify(bookings), 200)
    return res

@app.route("/bookings/<userid>", methods=['GET'])
def get_booking_for_user(userid):
    for booking in bookings:
        if str(booking["userid"]) == str(userid):
            res = make_response(jsonify(booking),200)
            return res
    return make_response(jsonify({"error":"User booking not found"}),400)

@app.route("/bookings/<userid>", methods=['POST'])
def add_booking_byuser(userid):
   new_booking  = request.get_json()

   url = f"http://showtime:3202/showtimes/{new_booking["date"]}"
   showtime = requests.get(url).json()

   if "error" not in showtime and new_booking["movieid"] in showtime["movies"]:
      for booking in bookings:
         if booking["userid"] == userid: 
               for booking_date in booking["dates"]:
                  if booking_date["date"] == new_booking["date"]:  
                     for movie in booking_date["movies"]:
                           if movie == new_booking["movieid"]:
                              return make_response(jsonify({"error": "User already booked this movie"}), 400)
                     booking_date["movies"].append(new_booking["movieid"])
                     write(bookings)  
                     return make_response(jsonify({"message": "Booking updated successfully"}), 200)
               booking["dates"].append({
                  "date": new_booking["date"],
                  "movies": [new_booking["movieid"]]
               })
               write(bookings) 
               return make_response(jsonify({"message": "New date added and movie booked successfully"}), 200)

      bookings.append({
         "userid": userid,
         "dates": [{
               "date": new_booking["date"],
               "movies": [new_booking["movieid"]]
         }]
      })
      write(bookings)  # Sauvegarde des modifications dans le fichier JSON
      return make_response(jsonify({"message": "New user and booking created successfully"}), 200)
   else:
      return make_response(jsonify({"error": "booking as not a showtime"}), 400)


def write(bookings):
    with open('./databases/bookings.json'.format("."), 'w') as f:
        json.dump(bookings, f)


if __name__ == "__main__":
   print("Server running in port %s"%(PORT))
   app.run(host=HOST, port=PORT)


# if __name__ == '__main__':
#     serve()
