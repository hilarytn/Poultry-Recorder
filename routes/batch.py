from datetime import datetime
from flask import Blueprint, request, jsonify
from extensions import db
from models.batch import Batch
from schemas.batch_schema import BatchSchema
from flask_jwt_extended import jwt_required, get_jwt_identity

batches_bp = Blueprint('batches', __name__)
batch_schema = BatchSchema()
batches_schema = BatchSchema(many=True)

# GET /batches - Retrieve all batches
@batches_bp.route('/batches', methods=['GET'])
def get_batches():
    batches = Batch.query.all()
    return jsonify(batches_schema.dump(batches)), 200

# GET /batches/<id> - Retrieve a specific batch
@batches_bp.route('/batches/<id>', methods=['GET'])
def get_batch(id):
    batch = Batch.query.get(id)
    if not batch:
        return jsonify({"message": "Batch not found"}), 404
    return jsonify(batch_schema.dump(batch)), 200

# POST /batches - Create a new batch
@batches_bp.route('/batche/add', methods=['POST'])
@jwt_required()
def create_batch():
    data = request.get_json()
    user_id = get_jwt_identity()

    # Validate input data
    errors = batch_schema.validate(data)
    if errors:
        return jsonify(errors), 400

    # Create a new batch
    new_batch = Batch(
        name=data['name'],
        quantity=data['quantity'],
        mortality=data['mortality'],
        feed_id=data.get('feed_id'),
        user_id=data['user_id'],
        batch_number=f"{data['user_id']}/{datetime.now().strftime('%Y%m%d%H%M%S')}"  # Example batch number format
    )

    db.session.add(new_batch)
    db.session.commit()
    return jsonify({"message": "Batch created successfully", "batch": batch_schema.dump(new_batch)}), 201

# PUT /batches/<id> - Update a batch
@batches_bp.route('/batches/<id>', methods=['PUT'])
def update_batch(id):
    batch = Batch.query.get(id)
    if not batch:
        return jsonify({"message": "Batch not found"}), 404

    data = request.get_json()

    # Validate input data
    errors = batch_schema.validate(data, partial=True)  # Allow partial updates
    if errors:
        return jsonify(errors), 400

    # Update batch fields
    batch.name = data.get('name', batch.name)
    batch.start_date = data.get('start_date', batch.start_date)
    batch.end_date = data.get('end_date', batch.end_date)
    batch.quantity = data.get('quantity', batch.quantity)
    batch.status = data.get('status', batch.status)
    batch.mortality = data.get('mortality', batch.mortality)
    batch.feed_id = data.get('feed_id', batch.feed_id)

    db.session.commit()
    return jsonify({"message": "Batch updated successfully", "batch": batch_schema.dump(batch)}), 200

# DELETE /batches/<id> - Delete a batch
@batches_bp.route('/batches/<id>', methods=['DELETE'])
def delete_batch(id):
    batch = Batch.query.get(id)
    if not batch:
        return jsonify({"message": "Batch not found"}), 404

    db.session.delete(batch)
    db.session.commit()
    return jsonify({"message": "Batch deleted successfully"}), 200