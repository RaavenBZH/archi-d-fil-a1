from flask import Flask, render_template, request, jsonify, make_response
import requests
import json
from werkzeug.exceptions import NotFound

app = Flask(__name__)

PORT = 3203
HOST = '0.0.0.0'

with open('{}/databases/users.json'.format("."), "r") as jsf:
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

if __name__ == "__main__":
   print("Server running in port %s"%(PORT))
   app.run(host=HOST, port=PORT)
