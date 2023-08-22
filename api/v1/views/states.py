#!/usr/bin/python3

from api.v1.views import app_views
from flask import jsonify, abort, make_response, request
from models import storage
from models.state import State

@app_views.route('/states', methods=['GET'], strict_slashes=False)
def states():
    """ Retrieves the list of all State objects """
    states = storage.all(State)
    return jsonify([obj.to_dict() for obj in states.values()])

@app_views.route("/states/<state_id>",  methods=["GET"], strict_slashes=False)
def state_by_id(state_id):
    """ Retrieves a State object """
    state = storage.get("State", state_id)

    if not state:
        print("State not found")
        abort(404)

    return jsonify(state.to_dict())   

@app_views.route('/states/<state_id>', methods=['DELETE'],
                 strict_slashes=False)
def delete_state(state_id):
    """ Deletes a State object """
    state = storage.get("State", state_id)
    if not state:
        abort(404)
    state.delete()
    storage.save()
    return make_response(jsonify({}), 200)

@app_views.route('/states', methods=['POST'], strict_slashes=False)
def create_state():
    """ Creates a State object """
    new_state = request.get_json()
    if not new_state:
        abort(400, "Not a JSON")
    if "name" not in new_state:
        abort(400, "Missing name")
    state = State(**new_state)
    storage.new(state)
    storage.save()
    return make_response(jsonify(state.to_dict()), 201)

@app_views.route('/states/<state_id>', methods=['PUT'], strict_slashes=False)
def update_state(state_id):
    """ Updates a State object """
    state = storage.get("State", state_id)
    if not state:
        abort(404)

    body_request = request.get_json()
    if not body_request:
        abort(400, "Not a JSON")

    for key, value in body_request.items():
        if key != 'id' and key != 'created_at' and key != 'updated_at':
            setattr(state, key, value)

    storage.save()
    return make_response(jsonify(state.to_dict()), 200)
