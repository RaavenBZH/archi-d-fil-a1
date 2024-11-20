from ariadne import graphql_sync, make_executable_schema, load_schema_from_path, ObjectType, QueryType, MutationType
from flask import Flask, request, jsonify, make_response

import resolvers as r
import os

PORT = 3200
HOST = '0.0.0.0'
app = Flask(__name__)
path = os.getcwd()

# todo create elements for Ariadne
type_defs = load_schema_from_path(f'{path}/movie.graphql')
query = QueryType()
mutation = MutationType()
movie = ObjectType('Movie')
info = ObjectType('Info')

query.set_field('movies_info',r.movies_info)
query.set_field('all_movies', r.all_movies)
query.set_field('movie_with_id', r.movie_with_id)
query.set_field('movie_with_title', r.movie_with_title)
query.set_field('movie_with_director', r.movie_with_director)
query.set_field('movie_with_rate', r.movie_with_rate)
mutation.set_field('delete_movie_with_id', r.delete_movie_with_id)
mutation.set_field('update_movie_rating', r.update_movie_rating)
mutation.set_field('add_movie', r.add_movie)
schema = make_executable_schema(type_defs, movie, query, info, mutation)

# root message
@app.route("/", methods=['GET'])
def home():
    return make_response("<h1 style='color:blue'>Welcome to the Movie service!</h1>",200)

@app.route('/graphql', methods=['POST'])
def graphql_server():
    data = request.get_json()
    success, result = graphql_sync(
                        schema,
                        data,
                        context_value=None,
                        debug=app.debug
                    )
    
    if success:
        status_code = 200
    else:
        status_code = 400

    return jsonify(result), status_code

if __name__ == "__main__":
    print("Server running in port %s"%(PORT))
    app.run(host=HOST, port=PORT)