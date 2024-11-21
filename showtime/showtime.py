from flask import Flask, render_template, request, jsonify, make_response
import json
from werkzeug.exceptions import NotFound

app = Flask(__name__)

# Constants
PORT = 3202
HOST = '0.0.0.0'
SCHEDULE_FILE = './databases/times.json'
ERROR_SCHEDULE_NOT_FOUND = {"error": "Schedule date not found"}

# Load schedule from JSON file
with open(SCHEDULE_FILE, "r") as jsf:
    schedule = json.load(jsf)["schedule"]

def write(times):
    """Helper function to write schedule to JSON file."""
    with open(SCHEDULE_FILE, 'w') as f:
        json.dump({"schedule": times}, f)

@app.route("/", methods=['GET'])
def home():
    """Home route to welcome users."""
    return "<h1 style='color:blue'>Welcome to the Showtime service!</h1>"

@app.route("/showtimes", methods=['GET'])
def get_schedule():
    """Route to get the entire schedule."""
    return make_response(jsonify(schedule), 200)

@app.route("/showtimes/<date>", methods=['GET'])
def get_movies_bydate(date):
    """Route to get movies by a specific date."""
    for s in schedule:
        if str(s["date"]) == str(date):
            return make_response(jsonify(s), 200)
    return make_response(jsonify(ERROR_SCHEDULE_NOT_FOUND), 400)

@app.route("/add_schedule", methods=['POST'])
def add_schedule():
    """Route to add a new schedule or update an existing one."""
    req = request.get_json()
    for s in schedule:
        if s["date"] == req["date"]:
            # Add new movies to the existing date
            for movie in req["movies"]:
                if movie not in s["movies"]:
                    s["movies"].append(movie)
            write(schedule)
            return make_response(jsonify({
                "message": "Schedule updated.",
                "data": {
                    "date": req["date"],
                    "movies": req["movies"]
                },
            }), 200)

    # Create a new schedule if the date does not exist
    new_schedule = {
        "date": req["date"],
        "movies": list(req["movies"])
    }
    schedule.append(new_schedule)
    write(schedule)
    return make_response(jsonify({
        "message": "Schedule created.",
        "data": {
            "date": req["date"],
            "movies": req["movies"]
        },
    }), 200)

if __name__ == "__main__":
    print(f"Server running on port {PORT}")
    app.run(host=HOST, port=PORT)