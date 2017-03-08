from graph import Graph
from scraper import Scraper
from flask import Flask, jsonify, request, abort
from vertex import Vertex
import logging
import urllib


logging.basicConfig(filename='test.log', level=logging.DEBUG)
running = True

app = Flask(__name__)
graph = Graph()
graph.open_json('data/default.json')


def get_nodes(attr, attr_name, want_actor, is_with):
    return_nodes = []
    for actor in graph:
        if actor.is_actor == want_actor:
            if not hasattr(actor, attr):
                break
            if type(getattr(actor, attr)) is int:
                if (getattr(actor, attr) == attr_name) == is_with:
                    return_nodes.append(actor.node_id + " (" + attr + ": " + str(getattr(actor, attr)) + ")")
            elif (attr_name.lower() in getattr(actor, attr).lower()) == is_with and attr == 'node_id':
                return_nodes.append(actor.node_id)
            elif (attr_name.lower()  in getattr(actor, attr).lower()) == is_with:
                return_nodes.append(actor.node_id + " (" + attr + ": " + getattr(actor, attr) + ")")
    return jsonify({attr: return_nodes})


def get_nodes_without(attr, attr_name, want_actor):
    return get_nodes(attr, attr_name, want_actor, False)


def get_nodes_with(attr, attr_name, want_actor):
    return get_nodes(attr, attr_name, want_actor, True)


@app.route('/actor/<string:query_type>/<string:attr>/<string:attr_name>', methods=['GET'])
def get_actors(query_type, attr, attr_name):
    if query_type.lower() == 'with':
        if attr_name.lower() == 'all' and attr.lower() == 'all':
            return get_nodes_without('node_id', 'not_a_real_actor_name', True)
        if attr == 'name':
            attr = 'node_id'
        return get_nodes_with(attr, attr_name, True)
    elif 'without' == query_type.lower():
            if attr == 'name':
                attr = 'node_id'
            return get_nodes_without(attr, attr_name, True)
    return "Not a real query"


@app.route('/movie/<string:query_type>/<string:attr>/<string:attr_name>', methods=['GET'])
def get_movies(query_type, attr, attr_name):
    if query_type.lower() == 'with':
        if attr_name.lower() == 'all' and attr.lower() == 'all':
            return get_nodes_without('node_id', 'not_a_real_actor_name', False)
        if attr == 'name':
            attr = 'node_id'
        return get_nodes_with(attr, attr_name, False)
    elif 'without' == query_type.lower():
        if attr == 'name':
            attr = 'node_id'
        return get_nodes_without(attr, attr_name, False)
    return "Not a real query"


def post_node(json):
    node = Vertex("new param", True, -1)
    try:
        node.open_json(json)
    except TypeError:
        return "It was not parsed."

    graph.add_vertex(node)
    return node.node_id + " is parsed."


@app.route('/actor', methods=['POST'])
def post_actor():
    return post_node(request.json)


@app.route('/movie', methods=['POST'])
def post_movie():
    return post_node(request.json)


@app.route('/actor/<string:name>', methods=['DELETE'])
def remove_actor(name):
    return graph.remove_vertex(name)


@app.route('/movie/<string:name>', methods=['DELETE'])
def remove_movie(name):
    return graph.remove_vertex(name)


def update_node(node_name, attr, attr_name, want_actor):
    if node_name not in graph.vertex_list.keys():
        return "Did not find " + node_name
    actor = graph.vertex_list[node_name]
    if actor.is_actor == want_actor:
        if not hasattr(actor, attr):
            return node_name + " did not contain " + str(attr)
        setattr(actor, attr, attr_name)
        return node_name + " updated!"
    return "Did not process the update"

@app.route('/movie/<string:movie_name>/<string:attr>/<string:attr_name>', methods=['PUT'])
def update_movie(movie_name, attr, attr_name):
    return update_node(movie_name, attr, attr_name, False)

@app.route('/movie/<string:actor_name>/<string:attr>/<string:attr_name>', methods=['PUT'])
def update_actor(movie_name, attr, attr_name, ):
    return update_node(movie_name, attr, attr_name, True)

'''
@app.route('/actor/get/<string:attr>/<string:attr_name>', methods=['GET'])
def get_actors(attr, attr_name):
    if attr == 'remove':
        if remove_actor(attr_name) == 0:
            return attr_name + " removed."
        else:
            return attr_name + " was not in database."
    elif 'without_' in attr and len(attr) > 8:
        attr = attr[8:]
        if attr == 'name':
            attr = 'node_id'
        return get_actors_without(attr, attr_name)
    elif 'with_' in attr and len(attr) > 5:
        attr = attr[5:]
        if attr_name == 'all':
            return get_actors_without('node_id', 'not_a_real_actor_name')
        if attr == 'name':
            attr = 'node_id'
        return get_actors_with(attr, attr_name )
    else:
        return "Did not understand query " + attr

'''



@app.route('/')
def index():
    return_string = "Welcome to ahchang6's Wikipedia API<br/>"
    return_string += "1. [actor/movie]/remove/[name] removes the [name] supplied from [actor/movie] database.<br/>"
    return_string += "2. [actor/movie]/without_[attr]/[attr_name] returns the all [actor/movie] without [attr] = [attr_name].<br/>"
    return_string += "3. [actor/movie]/with_[attr]/[attr_name] returns the all [actor/movie] with [attr] = [attr_name].<br/>"
    return_string += "-------if [attr_name] = all: return all actors"
    return_string += "4. [actor/movie]/put_[attr]/[attr_name], updates the attribute of the [actor/movie]<br/>"
    return_string += "5. [actor/movie]/add/[json_file of the actor/movie], parses the json file provided and adds the actor/movie into databse <br/>"
    return return_string


if __name__ == '__main__':
    app.run(debug=True)
