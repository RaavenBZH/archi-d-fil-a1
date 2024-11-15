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

PORT = 3203
HOST = '0.0.0.0'

with open('{}/data/users.json'.format("."), "r") as jsf:
   users = json.load(jsf)["users"]

def get_booking_stub():
    channel = grpc.insecure_channel('booking:3201')
    return booking_pb2_grpc.BookingServiceStub(channel)


@app.route("/", methods=['GET'])
def home():
    return "<h1 style='color:blue'>Welcome to the User service!</h1>"

@app.route("/users", methods=['GET'])
def get_users():
    print('ok')
    return make_response(jsonify(users), 200)

@app.route("/usersbyid/<userid>", methods=['GET'])
def get_user_byid(userid):
    for user in users:
        if str(user["id"]) == str(userid):
            try:
                # Create a gRPC request for the user ID
                booking_stub = get_booking_stub()
                request = booking_pb2.UserIdRequest(userid=userid)
                response = booking_stub.GetBookingsForUser(request)

                # Process response
                user["bookings"] = [
                    {
                        "date": date_item.date,
                        "movies": date_item.movies
                    }
                    for date_item in response.dates
                ]
            except grpc.RpcError as e:
                print(f"Error connecting to booking service: {e}")
                return make_response(jsonify({"error": "Error connecting to booking service"}), 500)
            return make_response(jsonify(user), 200)
    return make_response(jsonify({"error": "User ID not found"}), 400)

@app.route("/usersbyname/<username>", methods=['GET'])
def get_user_byname(username):
    for user in users:
        if str(user["name"]) == str(username):
            try:
                # Create a gRPC request for the user ID
                booking_stub = get_booking_stub()
                request = booking_pb2.UserIdRequest(userid=user["id"])
                response = booking_stub.GetBookingsForUser(request)

                # Process response
                user["bookings"] = [
                    {
                        "date": str(date_item.date),
                        "movies": list(date_item.movies)
                    }
                    for date_item in response.dates
                ]
            except grpc.RpcError as e:
                print(f"Error connecting to booking service: {e}")
                return make_response(jsonify({"error": "Error connecting to booking service"}), 500)
            return make_response(jsonify(user), 200)
    return make_response(jsonify({"error": "User name not found"}), 400)

@app.route("/users/movies/<userid>", methods=['GET'])
def get_user_movies_byid(userid):
    for user in users:
        if str(user["id"]) == str(userid):
            infos = []
            try:
                # gRPC request for user bookings
                booking_stub = get_booking_stub()
                request = booking_pb2.UserIdRequest(userid=userid)
                response = booking_stub.GetBookingsForUser(request)

                # Process booking data
                for date_item in response.dates:
                    obj = {
                        date_item.date: list(date_item.movies)
                    }
                    infos.append(obj)
            except grpc.RpcError as e:
                print(f"Error connecting to booking service: {e}")
                return make_response(jsonify({"error": "Error connecting to booking service"}), 500)

            # Fetch movie details from the movie service
            for obj in infos:
                for date, movies in obj.items():
                    movies_by_date = []
                    for movie in movies:
                        try:
                            query = '''
                                query {
                                    movie_with_id(_id: "''' + movie + '''") {
                                        id
                                        title
                                        rating
                                        director
                                    }
                                }
                            '''
                            movie_data = requests.post("http://movie:3200/graphql", json={"query": query}).json()
                            movies_by_date.append(movie_data)
                        except requests.exceptions.RequestException as e:
                            print(f"Error connecting to movie service: {e}")
                            return make_response(jsonify({"error": "Error connecting to movie service"}), 500)

                    obj[date] = movies_by_date

            user["movies"] = infos
            return make_response(jsonify(user), 200)
    return make_response(jsonify({"error": "User ID not found"}), 400)

if __name__ == "__main__":
    print("Server running on port %s" % (PORT))
    app.run(host=HOST, port=PORT)


