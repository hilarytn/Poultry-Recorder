from flask import Blueprint, jsonify, request
from extensions import db
from models.feed import Feed
from schemas.feed_schema import FeedSchema

feeds_bp = Blueprint('feeds', __name__)

# Initialize the schema
feed_schema = FeedSchema()
feeds_schema = FeedSchema(many=True)

@feeds_bp.route('/feeds', methods=['GET'])
def get_feeds():
    feeds = Feed.query.all()
    if not feeds:
        return jsonify({"message": "No feeds found"}), 404

    # Serialize feeds using the schema
    feeds_data = feeds_schema.dump(feeds)
    return jsonify(feeds_data), 200

@feeds_bp.route('/feeds/<id>', methods=['GET'])
def get_feed(id):
    feed = Feed.query.get(id)
    if not feed:
        return jsonify({"message": "Feed not found"}), 404

    # Serialize a single feed
    feed_data = feed_schema.dump(feed)
    return jsonify(feed_data), 200

@feeds_bp.route('/feeds', methods=['POST'])
def add_feed():
    data = request.get_json()
    
    # Validate the input using the schema
    errors = feed_schema.validate(data)
    if errors:
        return jsonify(errors), 400

    new_feed = Feed(
        title=data['title'],
        content=data['content']
    )
    db.session.add(new_feed)
    db.session.commit()

    # Serialize the newly created feed
    feed_data = feed_schema.dump(new_feed)
    return jsonify({"message": "Feed added successfully", "feed": feed_data}), 201

@feeds_bp.route('/feeds/<id>', methods=['PUT'])
def update_feed(id):
    feed = Feed.query.get(id)
    if not feed:
        return jsonify({"message": "Feed not found"}), 404

    data = request.get_json()

    # Validate the input using the schema
    errors = feed_schema.validate(data)
    if errors:
        return jsonify(errors), 400

    # Update the feed
    feed.title = data.get('title', feed.title)
    feed.content = data.get('content', feed.content)
    db.session.commit()

    # Serialize the updated feed
    feed_data = feed_schema.dump(feed)
    return jsonify({"message": "Feed updated successfully", "feed": feed_data}), 200

@feeds_bp.route('/feeds/<id>', methods=['DELETE'])
def delete_feed(id):
    feed = Feed.query.get(id)
    if not feed:
        return jsonify({"message": "Feed not found"}), 404

    db.session.delete(feed)
    db.session.commit()
    return jsonify({"message": "Feed deleted successfully"}), 200
