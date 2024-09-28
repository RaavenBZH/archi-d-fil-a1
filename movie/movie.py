from flask import Flask, render_template, request, jsonify, make_response
import json
import sys
from werkzeug.exceptions import NotFound

app = Flask(__name__)

PORT = 3200
HOST = '0.0.0.0'

def write(movies):
    with open('./databases/movies.json'.format("."), 'w') as f:
        json.dump(movies, f)

with open('./databases/movies.json'.format("."), 'r') as jsf:
   movies = json.load(jsf)["movies"]

# root message
@app.route("/", methods=['GET'])
def home():
    return make_response("<h1 style='color:black'>Welcome to the Movie service!</h1>",200)

# @app.route("/template", methods=['GET'])
# def template():
#     return make_response(render_template('index.html', body_text='This is my HTML template for Movie service'),200)

@app.route("/json", methods=['GET'])
def get_json():
    res = make_response(jsonify(movies), 200)
    return res

@app.route("/movies/<movieid>", methods=['GET'])
def get_movie_byid(movieid):
    for movie in movies:
        if str(movie["id"]) == str(movieid):
            res = make_response(jsonify(movie),200)
            return res
    return make_response(jsonify({"error":"Movie ID not found"}),400)

@app.route("/movies/<movieid>", methods=['DELETE'])
def del_movie(movieid):
    for movie in movies:
        if str(movie["id"]) == str(movieid):
            movies.remove(movie)
            return make_response(jsonify(movie),200)

    res = make_response(jsonify({"error":"movie ID not found"}),400)
    return res

@app.route("/movies/<movieid>/<rate>", methods=['PUT'])
def update_movie_rating(movieid, rate):
    for movie in movies:
        if str(movie["id"]) == str(movieid):
            movie["rating"] = rate
            res = make_response(jsonify(movie),200)
            return res

    res = make_response(jsonify({"error":"movie ID not found"}),201)
    return res

@app.route("/moviesbytitle", methods=['GET'])
def get_movie_bytitle():
    result = []
    if request.args:
        req = request.args
        for movie in movies:
            if str(movie["title"]) == str(req["title"]):
                result.append(movie)

    if not result:
        res = make_response(jsonify({"error":"movie title not found"}),400)
    else:
        res = make_response(jsonify(result),200)
    return res

@app.route("/moviesbydirector", methods=['GET'])
def get_movie_bydirector():
    result = []
    if request.args:
        req = request.args
        for movie in movies:
            if str(movie["director"]) == str(req["director"]):
                result.append(movie)

    if not result:
        res = make_response(jsonify({"error":"movie director not found"}),400)
    else:
        res = make_response(jsonify(result),200)
    return res

@app.route("/moviesbyrate", methods=['GET'])
def get_movie_byrate():
    result = []
    epsilon = 0.5
    if request.args:
        req = request.args
        for movie in movies:
            rate = float(req["rate"])
            
            cond1 = rate - epsilon <= movie["rating"]
            cond2 = rate + epsilon >= movie["rating"]

            if cond1 and cond2:
                result.append(movie)

    if not result:
        res = make_response(jsonify({"error":"movie rate not found"}),400)
    else:
        res = make_response(jsonify(result),200)
    return res

@app.route("/addmovie/<movieid>", methods=['POST'])
def add_movie(movieid):
    req = request.get_json()

    for movie in movies:
        if str(movie["id"]) == str(movieid):
            return make_response(jsonify({"error":"movie ID already exists"}),409)

    movies.append(req)
    write(movies)
    res = make_response(jsonify({"message":"movie added"}),200)
    return res

@app.route("/help", methods=['GET'])
def help():
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
    #p = sys.argv[1]
    print("Server running in port %s"%(PORT))
    app.run(host=HOST, port=PORT)
