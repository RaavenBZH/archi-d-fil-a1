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

if __name__ == "__main__":
    print(f"Server running on port {PORT}")
    app.run(host=HOST, port=PORT)