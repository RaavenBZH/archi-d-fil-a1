from flask import Flask, render_template, request, jsonify, make_response
import requests
import json
from werkzeug.exceptions import NotFound

app = Flask(__name__)

# Constants
PORT = 3201
HOST = '0.0.0.0'
BOOKINGS_FILE = './databases/bookings.json'
ERROR_USER_NOT_FOUND = {"error": "User booking not found"}
ERROR_BOOKING_EXISTS = {"error": "User already booked this movie"}
ERROR_NO_SHOWTIME = {"error": "No showtime available for the booking"}

# Load bookings from JSON file
with open(BOOKINGS_FILE, "r") as jsf:
    bookings = json.load(jsf)["bookings"]

@app.route("/", methods=['GET'])
def home():
    """Home route to welcome users."""
    return "<h1 style='color:blue'>Welcome to the Booking service!</h1>"

@app.route("/bookings", methods=['GET'])
def get_json():
    """Route to get all bookings."""
    return make_response(jsonify(bookings), 200)

@app.route("/bookings/<userid>", methods=['GET'])
def get_booking_for_user(userid):
    """Route to get bookings for a specific user."""
    for booking in bookings:
        if str(booking["userid"]) == str(userid):
            return make_response(jsonify(booking), 200)
    return make_response(jsonify(ERROR_USER_NOT_FOUND), 400)

@app.route("/bookings/<userid>", methods=['POST'])
def add_booking_byuser(userid):
    """Route to add a booking for a specific user."""
    new_booking = request.get_json()
    showtime = get_showtime(new_booking['date'])

    if "error" not in showtime and new_booking["movieid"] in showtime["movies"]:
        return handle_booking(userid, new_booking)
    else:
        return make_response(jsonify(ERROR_NO_SHOWTIME), 400)

def get_showtime(date):
    """Helper function to get showtime for a specific date."""
    url = f"http://showtime:3202/showtimes/{date}"
    return requests.get(url).json()

def handle_booking(userid, new_booking):
    """Helper function to handle booking logic."""
    for booking in bookings:
        if booking["userid"] == userid:
            for booking_date in booking["dates"]:
                if booking_date["date"] == new_booking["date"]:
                    if new_booking["movieid"] in booking_date["movies"]:
                        return make_response(jsonify(ERROR_BOOKING_EXISTS), 400)
                    booking_date["movies"].append(new_booking["movieid"])
                    write_bookings()
                    return make_response(jsonify({"message": "Booking updated successfully"}), 200)
            booking["dates"].append({
                "date": new_booking["date"],
                "movies": [new_booking["movieid"]]
            })
            write_bookings()
            return make_response(jsonify({"message": "New date added and movie booked successfully"}), 200)

    bookings.append({
        "userid": userid,
        "dates": [{
            "date": new_booking["date"],
            "movies": [new_booking["movieid"]]
        }]
    })
    write_bookings()
    return make_response(jsonify({"message": "New user and booking created successfully"}), 200)

def write_bookings():
    """Helper function to write bookings to JSON file."""
    with open(BOOKINGS_FILE, 'w') as f:
        json.dump(bookings, f)

if __name__ == "__main__":
    print(f"Server running on port {PORT}")
    app.run(host=HOST, port=PORT)