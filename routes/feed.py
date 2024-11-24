from flask import Blueprint, jsonify, request
from extensions import db
from models.feed import Feed
from schemas.feed_schema import FeedSchema
from flask_jwt_extended import jwt_required, get_jwt_identity

feeds_bp = Blueprint('feeds', __name__)

# Initialize the schema
feed_schema = FeedSchema()
feeds_schema = FeedSchema(many=True)

@feeds_bp.route('/feeds', methods=['GET'])
@jwt_required()
def get_feeds():
    user_id = get_jwt_identity()
    feeds = Feed.query.filter_by(user_id=user_id).all()
    if not feeds:
        return jsonify({"message": "No feeds found"}), 404

    # Serialize the feeds
    feeds_data = feeds_schema.dump(feeds, many=True)

    return jsonify(feeds_data), 200



@feeds_bp.route('/feeds/<id>', methods=['GET'])
@jwt_required()
def get_feed(id):
    feed = Feed.query.get(id)
    if not feed:
        return jsonify({"message": "Feed not found"}), 404

    # Serialize a single feed
    feed_data = feed_schema.dump(feed)
    return jsonify(feed_data), 200

@feeds_bp.route('/feeds', methods=['POST'])
@jwt_required()
def add_feed():
    data = request.get_json()
    user_id = get_jwt_identity()
    
    # Validate the input using the schema
    errors = feed_schema.validate(data)
    if errors:
        return jsonify(errors), 400

    # Create a new feed with the updated fields
    new_feed = Feed(
        name=data['name'],
        description=data.get('description'),  # Optional field
        quantity=data['quantity'],
        user_id=user_id
    )
    db.session.add(new_feed)
    db.session.commit()

    # Serialize the newly created feed
    feed_data = feed_schema.dump(new_feed)
    return jsonify({"message": "Feed added successfully", "feed": feed_data}), 201

@feeds_bp.route('/feeds/<id>', methods=['PUT'])
@jwt_required()
def update_feed(id):
    user_id = get_jwt_identity()
    feed = Feed.query.filter_by(user_id=user_id, id=id).first()
    if not feed:
        return jsonify({"message": "Feed not found"}), 404

    data = request.get_json()

    # Partial update: Only validate the fields provided by the user
    partial_schema = FeedSchema(partial=True)  # Allows partial updates
    errors = partial_schema.validate(data)
    if errors:
        return jsonify(errors), 400

    # Update the feed with the fields that were provided
    feed.name = data.get('name', feed.name)
    feed.description = data.get('description', feed.description)
    feed.quantity = data.get('quantity', feed.quantity)

    # Commit changes to the database
    db.session.commit()

    # Serialize the updated feed
    feed_data = feed_schema.dump(feed)
    return jsonify({"message": "Feed updated successfully", "feed": feed_data}), 200


@feeds_bp.route('/feeds/<id>', methods=['DELETE'])
@jwt_required()
def delete_feed(id):
    user_id = get_jwt_identity()
    feed = Feed.query.filter_by(user_id=user_id, id=id).first()
    if not feed:
        return jsonify({"message": "Feed not found"}), 404

    db.session.delete(feed)
    db.session.commit()
    return jsonify({"message": "Feed deleted successfully"}), 200