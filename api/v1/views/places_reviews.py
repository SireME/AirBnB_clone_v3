#!/usr/bin/python3
"""Objects that handle all default RestFul API actions for reviews"""
from flask import abort, jsonify, make_response, request
from models.place import Place
from models.review import Review
from models import storage
from api.v1.views import app_views


@app_views.route(
        '/places/<place_id>/reviews',
        methods=['GET'], strict_slashes=False)
def get_reviews(place_id):
    """
    Retrieves the list of all Review objects for a Place
    """
    place = storage.get(Place, place_id)
    if not place:
        abort(404)

    reviews = [review.to_dict() for review in place.reviews]
    return jsonify(reviews)


@app_views.route('/reviews/<review_id>', methods=['GET'], strict_slashes=False)
def get_review(review_id):
    """
    Retrieves a Review object by ID
    """
    review = storage.get(Review, review_id)
    if not review:
        abort(404)

    return jsonify(review.to_dict())


@app_views.route(
        '/reviews/<review_id>',
        methods=['DELETE'], strict_slashes=False)
def delete_review(review_id):
    """
    Deletes a Review object by ID
    """
    review = storage.get(Review, review_id)
    if not review:
        abort(404)

    storage.delete(review)
    storage.save()

    return make_response(jsonify({}), 200)


@app_views.route(
        '/places/<place_id>/reviews',
        methods=['POST'], strict_slashes=False)
def create_review(place_id):
    """
    Creates a new Review for a Place
    """
    place = storage.get(Place, place_id)
    if not place:
        abort(404)

    if not request.get_json():
        abort(400, description="Not a JSON")

    data = request.get_json()
    if 'user_id' not in data:
        abort(400, description="Missing user_id")

    user = storage.get(User, data.get('user_id'))
    if not user:
        abort(404)

    if 'text' not in data:
        abort(400, description="Missing text")

    review = Review(**data)
    review.place_id = place.id
    review.save()

    return make_response(jsonify(review.to_dict()), 201)


@app_views.route('/reviews/<review_id>', methods=['PUT'], strict_slashes=False)
def update_review(review_id):
    """
    Updates a Review object by ID
    """
    review = storage.get(Review, review_id)
    if not review:
        abort(404)

    if not request.get_json():
        abort(400, description="Not a JSON")

    data = request.get_json()
    ignore_keys = ['id', 'user_id', 'place_id', 'created_at', 'updated_at']

    for key, value in data.items():
        if key not in ignore_keys:
            setattr(review, key, value)

    storage.save()

    return make_response(jsonify(review.to_dict()), 200)
