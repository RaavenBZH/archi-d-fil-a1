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
    response = []
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
                return make_response(jsonify({"error": "Error connecting to booking service"}), 500)
            return make_response(jsonify(response), 200)
    return make_response(jsonify({"error": "User ID not found"}), 400)


@app.route("/usersbyname/<username>", methods=['GET'])
def get_user_byname(username):
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
                return make_response(jsonify({"error": "Error connecting to booking service"}), 500)
            print(response)
            return make_response(jsonify(response), 200)
    return make_response(jsonify({"error": "User name not found"}), 400)

@app.route("/users/movies/<userid>", methods=['GET'])
def get_user_movies_byid(userid):
    """
    Fetch user bookings by user ID and retrieve detailed movie information.
    """
    # Vérification de l'existence de l'utilisateur
    user = next((u for u in users if str(u.get("id")) == str(userid)), None)
    if not user:
        return make_response(jsonify({"error": "User ID not found"}), 404)

    try:
        # Initialisation de la connexion gRPC pour les réservations
        booking_stub = get_booking_stub()
        request = booking_pb2.UserIdRequest(userid=userid)
        grpc_response = booking_stub.GetBookingsForUser(request)

        # Transformation des données de réservations
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

    # Récupération des détails des films via le service Movie
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

                # Ajouter les détails du film au résultat
                detailed_movies.append(movie_data.get("data", {}).get("movie_with_id", {}))
            except requests.exceptions.RequestException as e:
                error_message = f"Error connecting to movie service for movie ID {movie_id}: {e}"
                print(error_message)
                return make_response(jsonify({"error": error_message}), 500)

        # Remplace les IDs des films par leurs détails
        booking["movies"] = detailed_movies

    # Préparation de la réponse finale
    user_data = {
        "id": user["id"],
        "name": user["name"],
        "movies": bookings
    }

    return make_response(jsonify(user_data), 200)

if __name__ == "__main__":
    print("Server running on port %s" % (PORT))
    app.run(host=HOST, port=PORT)


