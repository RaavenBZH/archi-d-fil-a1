import json
import inspect

# Constants
MOVIES_FILE = './data/movies.json'

def movies_info(_, info):
    """Return a list of all function names in the current module."""
    res = []
    for name, obj in inspect.getmembers(__import__(__name__)):
        if inspect.isfunction(obj) and obj.__module__ == __name__:
            res.append({"route": name})
    return res

def all_movies(_, info):
    """Return a list of all movies."""
    result = []
    with open(MOVIES_FILE, "r") as file:
        movies = json.load(file)
        for movie in movies['movies']:
            result.append(movie)
    return result

def movie_with_id(_, info, _id):
    """Return a movie with a specific ID."""
    with open(MOVIES_FILE, "r") as file:
        movies = json.load(file)
        for movie in movies['movies']:
            if movie['id'] == _id:
                return movie

def movie_with_title(_, info, _title):
    """Return a movie with a specific title."""
    with open(MOVIES_FILE, "r") as file:
        movies = json.load(file)
        for movie in movies['movies']:
            if str(movie["title"]) == _title:
                return movie

def movie_with_director(_, info, _director):
    """Return a movie with a specific director."""
    with open(MOVIES_FILE, "r") as file:
        movies = json.load(file)
        for movie in movies['movies']:
            if str(movie["director"]) == _director:
                return movie

def movie_with_rate(_, info, _rate):
    """Return a list of movies with a specific rating within a tolerance."""
    epsilon = 0.5
    result_set = []
    with open(MOVIES_FILE, "r") as file:
        movies = json.load(file)
        for movie in movies['movies']:
            cond1 = float(movie["rating"]) - epsilon <= _rate
            cond2 = float(movie["rating"]) + epsilon >= _rate
            if cond1 and cond2:
                result_set.append(movie)
    return result_set

def delete_movie_with_id(_, info, _id):
    """Delete a movie with a specific ID."""
    with open(MOVIES_FILE, "r") as file:
        movies = json.load(file)
        for movie in movies['movies']:
            if movie['id'] == _id:
                movies["movies"].remove(movie)
                with open(MOVIES_FILE, 'w') as f:
                    json.dump(movies, f)
                return movie

def update_movie_rating(_, info, _id, _rate):
    """Update the rating of a movie with a specific ID."""
    with open(MOVIES_FILE, "r") as file:
        movies = json.load(file)
        for movie in movies['movies']:
            if movie['id'] == _id:
                movie["rating"] = _rate
                with open(MOVIES_FILE, 'w') as f:
                    json.dump(movies, f)
                return movie

def add_movie(_, info, _id, _title, _director, _rating):
    """Add a new movie if it does not already exist."""
    movie_exist = False
    with open(MOVIES_FILE, "r") as file:
        movies = json.load(file)
        for movie in movies['movies']:
            if movie["id"] == _id:
                movie_exist = True
    if not movie_exist:
        new_movie = {
            "id": _id,
            "title": _title,
            "director": _director,
            "rating": _rating,
        }
        movies["movies"].append(new_movie)
        with open(MOVIES_FILE, 'w') as f:
            json.dump(movies, f)
        return new_movie
    return None