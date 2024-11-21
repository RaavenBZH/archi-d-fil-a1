from flask import Flask, render_template, request, jsonify, make_response
import requests
import json
from werkzeug.exceptions import NotFound

app = Flask(__name__)

# Constants
PORT = 3203
HOST = '0.0.0.0'
USERS_FILE = './databases/users.json'
ERROR_USER_NOT_FOUND = {"error": "User ID not found"}
ERROR_USER_NAME_NOT_FOUND = {"error": "User name not found"}
ERROR_CONNECT_BOOKING = {"error": "Error connecting to booking service"}
ERROR_CONNECT_MOVIE = {"error": "Error connecting to movie service"}

# Load users from JSON file
with open(USERS_FILE, "r") as jsf:
   users = json.load(jsf)["users"]

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
            bookings = requests.get(f"http://booking:3201/bookings/{userid}").json()
            user["bookings"] = bookings
         except requests.exceptions.RequestException as e:
            print(f"Error connecting to booking service: {e}")
            return make_response(jsonify(ERROR_CONNECT_BOOKING), 500)
         return make_response(jsonify(user), 200)
   return make_response(jsonify(ERROR_USER_NOT_FOUND), 400)

@app.route("/usersbyname/<username>", methods=['GET'])
def get_user_byname(username):
   """Route to get a user by their name."""
   for user in users:
      if str(user["name"]) == str(username):
         try:
            bookings = requests.get(f"http://booking:3201/bookings/{user['id']}").json()
            user["bookings"] = bookings
         except requests.exceptions.RequestException as e:
            print(f"Error connecting to booking service: {e}")
            return make_response(jsonify(ERROR_CONNECT_BOOKING), 500)
         return make_response(jsonify(user), 200)
   return make_response(jsonify(ERROR_USER_NAME_NOT_FOUND), 400)

@app.route("/users/movies/<userid>", methods=['GET'])
def get_user_movies_byid(userid):
   """Route to get movies booked by a user by their ID."""
   for user in users:
      if str(user["id"]) == str(userid):
         infos = []
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
            return make_response(jsonify(ERROR_CONNECT_BOOKING), 500)

         for obj in infos:
            for date, movies in obj.items():
               movies_by_date = []
               for movie in movies:
                  try:
                     movie_data = requests.get(f"http://movie:3200/movies/{movie}").json()
                     movies_by_date.append(movie_data)
                  except requests.exceptions.RequestException as e:
                     print(f"Error connecting to movie service: {e}")
                     return make_response(jsonify(ERROR_CONNECT_MOVIE), 500)
               obj[date] = movies_by_date

         user["movies"] = infos
         return make_response(jsonify(user), 200)
   return make_response(jsonify(ERROR_USER_NOT_FOUND), 400)

if __name__ == "__main__":
   print(f"Server running on port {PORT}")
   app.run(host=HOST, port=PORT)