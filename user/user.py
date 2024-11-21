# REST API
from flask import Flask, render_template, request, jsonify, make_response
import requests
import json
from werkzeug.exceptions import NotFound
# CALLING gRPC requests
import grpc
from concurrent import futures

import os, sys
sys.path.append(os.path.join(os.path.dirname(__file__), 'booking'))

from booking import booking_pb2, booking_pb2_grpc

app = Flask(__name__)

# Constants
PORT = 3203
HOST = '0.0.0.0'
USERS_FILE = './data/users.json'
ERROR_USER_NOT_FOUND = {"error": "User ID not found"}
ERROR_USER_NAME_NOT_FOUND = {"error": "User name not found"}
ERROR_CONNECT_BOOKING = {"error": "Error connecting to booking service"}
ERROR_CONNECT_MOVIE = {"error": "Error connecting to movie service"}

# Load users from JSON file
with open(USERS_FILE, "r") as jsf:
   users = json.load(jsf)["users"]

def get_booking_stub():
   """Helper function to create a gRPC stub for the booking service."""
   channel = grpc.insecure_channel('booking:3201')
   return booking_pb2_grpc.BookingServiceStub(channel)

@app.route("/", methods=['GET'])
def home():
   """Home route to welcome users."""
   return "<h1 style='color:blue'>Welcome to the User service!</h1>"

@app.route("/users", methods=['GET'])
def get_users():
   """Route to get all users."""
   return make_response(jsonify(users), 200)

@app.route("/usersbyid/<userid>", methods=['GET'])
def get_user_byid(userid):
   """Route to get a user by their ID."""
   for user in users:
      if str(user["id"]) == str(userid):
         try:
            # Create a gRPC request for the user ID
            booking_stub = get_booking_stub()
            request = booking_pb2.UserIdRequest(userid=userid)
            responseBooking = booking_stub.GetBookingsForUser(request)

            # Process response
            bookings = [
               {
                  "date": str(date_item.date),
                  "movies": list(date_item.movies)
               }
               for date_item in responseBooking.dates
            ]

            response = {
               "user": {
                  "id": user["id"],
                  "name": user["name"]
               },
               "bookings": bookings
            }
         except grpc.RpcError as e:
            print(f"Error connecting to booking service: {e}")
            return make_response(jsonify(ERROR_CONNECT_BOOKING), 500)
         return make_response(jsonify(response), 200)
   return make_response(jsonify(ERROR_USER_NOT_FOUND), 400)

@app.route("/usersbyname/<username>", methods=['GET'])
def get_user_byname(username):
   """Route to get a user by their name."""
   for user in users:
      if str(user["name"]) == str(username):
         try:
            # Create a gRPC request for the user ID
            booking_stub = get_booking_stub()
            request = booking_pb2.UserIdRequest(userid=user["id"])
            responseBooking = booking_stub.GetBookingsForUser(request)

            # Process response
            bookings = [
               {
                  "date": str(date_item.date),
                  "movies": list(date_item.movies)
               }
               for date_item in responseBooking.dates
            ]

            response = {
               "user": {
                  "id": user["id"],
                  "name": user["name"]
               },
               "bookings": bookings
            }
         except grpc.RpcError as e:
            print(f"Error connecting to booking service: {e}")
            return make_response(jsonify(ERROR_CONNECT_BOOKING), 500)
         return make_response(jsonify(response), 200)
   return make_response(jsonify(ERROR_USER_NAME_NOT_FOUND), 400)

@app.route("/users/movies/<userid>", methods=['GET'])
def get_user_movies_byid(userid):
   """Route to fetch user bookings by user ID and retrieve detailed movie information."""
   user = next((u for u in users if str(u.get("id")) == str(userid)), None)
   if not user:
      return make_response(jsonify(ERROR_USER_NOT_FOUND), 404)

   try:
      # Initialize gRPC connection for bookings
      booking_stub = get_booking_stub()
      request = booking_pb2.UserIdRequest(userid=userid)
      grpc_response = booking_stub.GetBookingsForUser(request)

      # Transform booking data
      bookings = [
         {
            "date": str(date_item.date),
            "movies": [str(movie) for movie in date_item.movies]
         }
         for date_item in grpc_response.dates
      ]
   except grpc.RpcError as e:
      error_message = f"Error connecting to booking service: {e}"
      print(error_message)
      return make_response(jsonify({"error": error_message}), 500)

   # Retrieve movie details via the Movie service
   for booking in bookings:
      detailed_movies = []
      for movie_id in booking["movies"]:
         try:
            query = '''
                    query {
                        movie_with_id(_id: "%s") {
                            id
                            title
                            rating
                            director
                        }
                    }
                ''' % movie_id
            response = requests.post(
               "http://movie:3200/graphql",
               json={"query": query}
            )
            response.raise_for_status()
            movie_data = response.json()

            # Add movie details to the result
            detailed_movies.append(movie_data.get("data", {}).get("movie_with_id", {}))
         except requests.exceptions.RequestException as e:
            error_message = f"Error connecting to movie service for movie ID {movie_id}: {e}"
            print(error_message)
            return make_response(jsonify({"error": error_message}), 500)

      # Replace movie IDs with their details
      booking["movies"] = detailed_movies

   # Prepare the final response
   user_data = {
      "id": user["id"],
      "name": user["name"],
      "movies": bookings
   }

   return make_response(jsonify(user_data), 200)

if __name__ == "__main__":
   print(f"Server running on port {PORT}")
   app.run(host=HOST, port=PORT)