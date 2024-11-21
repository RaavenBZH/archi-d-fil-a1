from flask import Flask, render_template, request, jsonify, make_response
import json
import sys
from werkzeug.exceptions import NotFound

app = Flask(__name__)

# Constants
PORT = 3200
HOST = '0.0.0.0'
MOVIES_FILE = './databases/movies.json'
ERROR_MOVIE_NOT_FOUND = {"error": "Movie ID not found"}
ERROR_MOVIE_EXISTS = {"error": "Movie ID already exists"}
ERROR_MOVIE_TITLE_NOT_FOUND = {"error": "Movie title not found"}
ERROR_MOVIE_DIRECTOR_NOT_FOUND = {"error": "Movie director not found"}
ERROR_MOVIE_RATE_NOT_FOUND = {"error": "Movie rate not found"}

# Load movies from JSON file
with open(MOVIES_FILE, 'r') as jsf:
    movies = json.load(jsf)["movies"]

def write_movies():
    """Helper function to write movies to JSON file."""
    with open(MOVIES_FILE, 'w') as f:
        json.dump({"movies": movies}, f)

@app.route("/", methods=['GET'])
def home():
    """Home route to welcome users."""
    return make_response("<h1 style='color:black'>Welcome to the Movie service!</h1>", 200)

@app.route("/json", methods=['GET'])
def get_json():
    """Route to get all movies in JSON format."""
    return make_response(jsonify(movies), 200)

@app.route("/movies/<movieid>", methods=['GET'])
def get_movie_byid(movieid):
    """Route to get a movie by its ID."""
    for movie in movies:
        if str(movie["id"]) == str(movieid):
            return make_response(jsonify(movie), 200)
    return make_response(jsonify(ERROR_MOVIE_NOT_FOUND), 400)

@app.route("/movies/<movieid>", methods=['DELETE'])
def del_movie(movieid):
    """Route to delete a movie by its ID."""
    for movie in movies:
        if str(movie["id"]) == str(movieid):
            movies.remove(movie)
            write_movies()
            return make_response(jsonify(movie), 200)
    return make_response(jsonify(ERROR_MOVIE_NOT_FOUND), 400)

@app.route("/movies/<movieid>/<rate>", methods=['PUT'])
def update_movie_rating(movieid, rate):
    """Route to update the rating of a movie by its ID."""
    for movie in movies:
        if str(movie["id"]) == str(movieid):
            movie["rating"] = rate
            write_movies()
            return make_response(jsonify(movie), 200)
    return make_response(jsonify(ERROR_MOVIE_NOT_FOUND), 400)

@app.route("/moviesbytitle", methods=['GET'])
def get_movie_bytitle():
    """Route to get movies by title."""
    result = []
    if request.args:
        req = request.args
        for movie in movies:
            if str(movie["title"]) == str(req["title"]):
                result.append(movie)
    if not result:
        return make_response(jsonify(ERROR_MOVIE_TITLE_NOT_FOUND), 400)
    return make_response(jsonify(result), 200)

@app.route("/moviesbydirector", methods=['GET'])
def get_movie_bydirector():
    """Route to get movies by director."""
    result = []
    if request.args:
        req = request.args
        for movie in movies:
            if str(movie["director"]) == str(req["director"]):
                result.append(movie)
    if not result:
        return make_response(jsonify(ERROR_MOVIE_DIRECTOR_NOT_FOUND), 400)
    return make_response(jsonify(result), 200)

@app.route("/moviesbyrate", methods=['GET'])
def get_movie_byrate():
    """Route to get movies by rating."""
    result = []
    epsilon = 0.5
    if request.args:
        req = request.args
        for movie in movies:
            rate = float(req["rate"])
            if rate - epsilon <= movie["rating"] <= rate + epsilon:
                result.append(movie)
    if not result:
        return make_response(jsonify(ERROR_MOVIE_RATE_NOT_FOUND), 400)
    return make_response(jsonify(result), 200)

@app.route("/addmovie/<movieid>", methods=['POST'])
def add_movie(movieid):
    """Route to add a new movie by its ID."""
    req = request.get_json()
    for movie in movies:
        if str(movie["id"]) == str(movieid):
            return make_response(jsonify(ERROR_MOVIE_EXISTS), 409)
    movies.append(req)
    write_movies()
    return make_response(jsonify({"message": "Movie added"}), 200)

@app.route("/help", methods=['GET'])
def help():
    """Route to display available endpoints."""
    routes = {
        "/"                        : "GET - Root message",
        "/json"                    : "GET - Get all movies in JSON format",
        "/movies/<movieid>"        : "GET - Get a movie by its ID",
        "/movies/<movieid>"        : "DELETE - Delete a movie by its ID",
        "/movies/<movieid>/<rate>" : "PUT - Update the rating of a movie by its ID",
        "/moviesbytitle"           : "GET - Get movies by title",
        "/moviesbydirector"        : "GET - Get movies by director",
        "/moviesbyrate"            : "GET - Get movies by rating",
        "/addmovie/<movieid>"      : "POST - Add a new movie by its ID"
    }
    return make_response(jsonify(routes), 200)

if __name__ == "__main__":
    print(f"Server running on port {PORT}")
    app.run(host=HOST, port=PORT)