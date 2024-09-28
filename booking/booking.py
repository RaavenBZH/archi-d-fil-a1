from flask import Flask, render_template, request, jsonify, make_response
import requests
import json
from werkzeug.exceptions import NotFound

app = Flask(__name__)

PORT = 3201
HOST = '0.0.0.0'

with open('./databases/bookings.json'.format("."), "r") as jsf:
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
   try:
      showtime = requests.get(url).json()
   except Exception as e:
      return make_response(jsonify({"error": f"Showtime service not available : {url} et {e} " }), 503)
    # Si la date existe, procéder à l'ajout de la réservation
   for booking in bookings:
      if booking["userid"] == userid:
         for booking_date in booking["dates"]:
            if booking_date["date"] == new_booking["date"]:
               for movie in booking_date["movies"]:
                  if movie["movieid"] == new_booking["movieid"]:
                     return make_response(jsonify({"error": "User already booked"}), 400)
                  else:
                     booking_date["movies"].append(new_booking["movieid"])
                     write(bookings)
                     return make_response(jsonify(booking), 200)

   return make_response(jsonify({"error": "Date not found"}), 400)




def write(bookings):
    with open('./databases/movies.json'.format("."), 'w') as f:
        json.dump(bookings, f)


if __name__ == "__main__":
   print("Server running in port %s"%(PORT))
   app.run(host=HOST, port=PORT)
