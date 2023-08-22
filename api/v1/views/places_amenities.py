#!/usr/bin/python3

#!/usr/bin/python3
"""create a view for link between Place objects and Amenity objects."""
from api.v1.views import app_views
from flask import jsonify, abort, request
from models import storage, storage_t
from models.amenity import Amenity


@app_views.route('/places/<place_id>/amenities',
                 methods=['GET'], strict_slashes=False)
def get_all_amenities(place_id):
    '''Retrieves the list of all Amenity objects of a Place'''
    place = storage.get('Place', place_id)

    if not place:
        abort(400)

    if storage_t == 'db':
        return jsonify([amenity.to_dict() for amenity in place.amenities])

    return jsonify([amenity.to_dict() for amenity in place.amenities()])


@app_views.route('/places/<place_id>/amenities/<amenity_id>',
                 methods=['DELETE', 'POST'])
def handle_amenity(place_id, amenity_id):
    '''deletes and creates new amenity'''
    place = storage.get('Place', place_id)
    amenity = storage.get('Amenity', amenity_id)

    if not place or not amenity:
        abort(400)

    if storage_t == 'db':
        amenities_in_place = [amenity.id for amenity in place.amenities]
    else:
        amenities_in_place = [amenity.id for amenity in place.amenities()]

    if amenity.id not in amenities_in_place:
        abort(400)

    if request.method == 'DELETE':
        storage.delete(amenity)
        storage.save()
        return jsonify({}), 200

    if request.method == 'POST':
        if amenity.id in amenities_in_place:
            return jsonify(amenity.to_dict()), 200

        amenities_in_place.append(amenity)
        storage.save()
        return jsonify(amenity.to_dict()), 201
