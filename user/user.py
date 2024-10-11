# REST API
from flask import Flask, render_template, request, jsonify, make_response
import requests
import json
from werkzeug.exceptions import NotFound

# CALLING gRPC requests
# import grpc
# from concurrent import futures
# import booking_pb2
# import booking_pb2_grpc
# import movie_pb2
# import movie_pb2_grpc

# CALLING GraphQL requests
# todo to complete

app = Flask(__name__)

PORT = 3203
HOST = '0.0.0.0'

with open('{}/data/users.json'.format("."), "r") as jsf:
   users = json.load(jsf)["users"]

@app.route("/", methods=['GET'])
def home():
   return "<h1 style='color:blue'>Welcome to the User service!</h1>"

@app.route("/users", methods=['GET'])
def get_users():
   res = make_response(jsonify(users), 200)
   return res

@app.route("/usersbyid/<userid>", methods=['GET'])
def get_user_byid(userid):
   for user in users:
      if str(user["id"]) == str(userid):
         try:
            bookings = requests.get(f"http://booking:3201/bookings/{userid}").json()
            user["bookings"] = bookings
         except requests.exceptions.RequestException as e:
            print(f"Error connecting to booking service: {e}")
            return make_response(jsonify({"error": "Error connecting to booking service"}), 500)
         res = make_response(jsonify(user),200)
         return res
   return make_response(jsonify({"error": "User ID not found"}), 400)

@app.route("/usersbyname/<username>", methods=['GET'])
def get_user_byname(username):
   for user in users:
      if str(user["name"]) == str(username):
         try:
            bookings = requests.get(f"http://booking:3201/bookings/{user["id"]}").json()
            user["bookings"] = bookings
         except requests.exceptions.RequestException as e:
            print(f"Error connecting to booking service: {e}")
            return make_response(jsonify({"error": "Error connecting to booking service"}), 500)
         res = make_response(jsonify(user),200)
         return res
   return make_response(jsonify({"error":"User name not found"}),400)

@app.route("/users/movies/<userid>", methods=['GET'])
def get_user_movies_byid(userid):
   for user in users:
      if str(user["id"]) == str(userid):
         infos = []

         # Get movie and date with booking service
         try:
            bookings = requests.get(f"http://booking:3201/bookings/{userid}").json()
            if bookings["userid"] == userid:
               dates = bookings["dates"]
               for date in dates:
                  movies = []
                  for movie in date["movies"]:
                     movies.append(movie)
                  obj = {date["date"]: movies}
                  infos.append(obj)
         except requests.exceptions.RequestException as e:
            print(f"Error connecting to booking service: {e}")
            return make_response(jsonify({"error": "Error connecting to booking service"}), 500)

         # Get movie data
         for obj in infos:
            for date, movies in obj.items():
               movies_by_date = []
               for movie in movies:
                  try:
                     print("\n"*10)
                     print(movie)
                     query = '''
                        query {
                           movie_with_id(_id: "''' + movie +'''") {
                                 id
                                 title
                                 rating
                                 director
                           }
                        }
                     '''
                     print(query)
                     movie_data = requests.post("http://movie:3200/graphql", json= {"query" : query}).json()
                     print(movie_data)
                     movies_by_date.append(movie_data)
                  except requests.exceptions.RequestException as e:
                     print(f"Error connecting to movie service: {e}")
                     return make_response(jsonify({"error": "Error connecting to movie service"}), 500)

               obj[date] = movies_by_date

         user["movies"] = infos
         res = make_response(jsonify(user),200)
         return res
   return make_response(jsonify({"error": "User ID not found"}), 400)

if __name__ == "__main__":
   print("Server running in port %s"%(PORT))
   app.run(host=HOST, port=PORT)


