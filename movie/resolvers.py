import json
import inspect

def movie_info(_, info):
    res = []

    # read file functions
    for name, obj in inspect.getmembers(__import__(__name__)):
        if inspect.isfunction(obj) and obj.__module__ == __name__:
            res.append({"route" : name})
    
    return res

def movie_with_id(_,info,_id):
    with open('{}/data/movies.json'.format("."), "r") as file:
        movies = json.load(file)
        for movie in movies['movies']:
            if movie['id'] == _id:
                return movie

def movie_with_title(_, info, _title):
    with open('{}/data/movies.json'.format("."), "r") as file:
        movies = json.load(file)
        for movie in movies['movies']:
            if str(movie["title"]) == _title:
                return movie
            
def movie_with_director(_, info, _director):
    with open('{}/data/movies.json'.format("."), "r") as file:
        movies = json.load(file)
        for movie in movies['movies']:
            if str(movie["director"]) == _director:
                return movie
            
def movie_with_rate(_, info, _rate):
    epsilon = 0.5
    result_set = []
    with open('{}/data/movies.json'.format("."), "r") as file:
        movies = json.load(file)
        for movie in movies['movies']:
            cond1 = movie["rating"] - epsilon <= _rate
            cond2 = movie["rating"] + epsilon >= _rate
            if cond1 and cond2:
                result_set.append(movie)
    return result_set

def delete_movie_with_id(_,info,_id):
    with open('{}/data/movies.json'.format("."), "r") as file:
        movies = json.load(file)
        for movie in movies['movies']:
            if movie['id'] == _id:
                movies["movies"].remove(movie)
                with open('{}/data/movies.json'.format("."), 'w') as f:
                    json.dump(movies, f)
                return movie
            
def update_movie_rating(_,info,_id, _rate):
    with open('{}/data/movies.json'.format("."), "r") as file:
        movies = json.load(file)
        for movie in movies['movies']:
            if movie['id'] == _id:
                movie["rating"] = _rate
                with open('{}/data/movies.json'.format("."), 'w') as f:
                    json.dump(movies, f)
                return movie
            

