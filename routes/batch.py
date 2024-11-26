from datetime import datetime
from flask import Blueprint, request, jsonify
from extensions import db
from models.batch import Batch
from models.user import User
from schemas.batch_schema import BatchSchema
from flask_jwt_extended import jwt_required, get_jwt_identity

batches_bp = Blueprint('batches', __name__)
batch_schema = BatchSchema()
batches_schema = BatchSchema(many=True)

@batches_bp.route('/batches', methods=['GET'])
@jwt_required()
def get_user_batches():
    user_id = get_jwt_identity()  # Get the current user's ID from the JWT
    batches = Batch.query.filter_by(user_id=user_id).all()  # Filter by user_id
    
    if not batches:
        return jsonify({"message": "No batches found for this user"}), 404

    return jsonify(batches_schema.dump(batches, many=True)), 200


@batches_bp.route('/batch/<id>', methods=['GET'])
@jwt_required()
def get_batch(id):
    user_id = get_jwt_identity()
    batch = Batch.query.filter_by(id=id, user_id=user_id).first()

    if not batch:
        return jsonify({"message": "Batch not found"}), 404

    return jsonify(batch_schema.dump(batch)), 200

# POST /batches - Create a new batch
@batches_bp.route('/batch/add', methods=['POST'])
@jwt_required()
def create_batch():
    data = request.get_json()
    user_id = get_jwt_identity()

    # Validate input data
    errors = batch_schema.validate(data)
    if errors:
        return jsonify(errors), 400
    
    # Get the user's full name from the database
    user = User.query.get(user_id)
    if not user:
        return jsonify({"message": "User not found"}), 404

    # Generate initials from the user's full name
    user_full_name = user.fullname  # Assuming there's a 'full_name' column in User
    user_initials = ''.join(word[0].upper() for word in user_full_name.split())

    # Generate the current timestamp
    timestamp = datetime.now().strftime('%Y%m%dT%H%M%S')  # Format as YYYYMMDDTHHMMSS

    # Combine initials and timestamp for the batch number
    batch_number = f"{user_initials}{timestamp}"

    # Create a new batch
    new_batch = Batch(
        name=data['name'],
        quantity=data['quantity'],
        mortality=data['mortality'],
        feed_id=data.get('feed_id'),
        user_id=user_id,
        batch_number=batch_number
    )

    db.session.add(new_batch)
    db.session.commit()
    return jsonify({"message": "Batch created successfully", "batch": batch_schema.dump(new_batch)}), 201

# PUT /batches/<id> - Update a batch
@batches_bp.route('/batch/<id>', methods=['PUT'])
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
@batches_bp.route('/batch/<id>', methods=['DELETE'])
@jwt_required()
def delete_batch(id):
    user_id = get_jwt_identity()
    batch = Batch.query.filter_by(user_id=user_id).first()
    if not batch:
        return jsonify({"message": "Batch not found"}), 404

    db.session.delete(batch)
    db.session.commit()
    return jsonify({"message": "Batch deleted successfully"}), 200