#!/usr/bin/python3

from api.v1.views import app_views
from flask import jsonify, abort, make_response, request
from models import storage
from models.place import Place
from models.review import Review
from models.user import User

@app_views.route('/places/<place_id>/reviews', methods=['GET'],
                 strict_slashes=False)
def reviews_by_place(place_id):
    """ Retrieves the list of all Review objects """
    place = storage.get(Place, place_id)
    if not place:
        abort(404)
    return jsonify([review.to_dict() for review in place.reviews])

@app_views.route('/reviews/<review_id>', methods=['GET'], strict_slashes=False)
def retrieve_review_id(review_id):
    """ Retrieves a Review object """
    review = storage.get(Review, review_id)
    if not review:
        abort(404)
    return jsonify(review.to_dict())

@app_views.route('/reviews/<review_id>', methods=['DELETE'],
                 strict_slashes=False)
def delete_review(review_id):
    """ Deletes a Review object """
    review = storage.get(Review, review_id)
    if not review:
        abort(404)
    review.delete()
    storage.save()
    return make_response(jsonify({}), 200)

@app_views.route('/places/<place_id>/reviews', methods=['POST'],
                 strict_slashes=False)
def post_review(place_id):
    """
    Creates a Review
    """
    place = storage.get(Place, place_id)

    if not place:
        abort(404)

    if not request.get_json():
        abort(400, description="Not a JSON")

    if 'user_id' not in request.get_json():
        abort(400, description="Missing user_id")

    data = request.get_json()
    user = storage.get(User, data['user_id'])

    if not user:
        abort(404)

    if 'text' not in request.get_json():
        abort(400, description="Missing text")

    data['place_id'] = place_id
    instance = Review(**data)
    instance.save()
    return make_response(jsonify(instance.to_dict()), 201)


@app_views.route('/reviews/<review_id>', methods=['PUT'],
                 strict_slashes=False)
def update_review(review_id):
    """ Updates a Review object """
    review = storage.get(Review, review_id)
    if not review:
        abort(404)

    body_request = request.get_json()
    if not body_request:
        abort(400, "Not a JSON")

    for k, v in body_request.items():
        if k not in ['id', 'user_id', 'place_id',
                     'created_at', 'updated_at']:
            setattr(review, k, v)

    storage.save()
    return make_response(jsonify(review.to_dict()), 200)
