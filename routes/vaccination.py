from datetime import datetime
from flask import Blueprint, request, jsonify
from extensions import db
from models.batch import Batch
from models.user import User
from models.vaccination import Vaccination
from schemas.vaccination_schema import VaccinationSchema
from flask_jwt_extended import jwt_required, get_jwt_identity

vaccination_bp = Blueprint('vaccination', __name__)
vaccination_schema = VaccinationSchema()
vaccinations_schema = VaccinationSchema(many=True)

# GET /vaccinations - Retrieve all vaccinations for the authenticated user
@vaccination_bp.route('/all', methods=['GET'])
@jwt_required()
def get_vaccinations():
    user_id = get_jwt_identity()
    vaccinations = Vaccination.query.filter_by(user_id=user_id).all()
    
    if not vaccinations:
        return jsonify({"message": "No vaccinations found"}), 404
    
    return jsonify(vaccinations_schema.dump(vaccinations)), 200

# GET /vaccinations/<id> - Retrieve details of a specific vaccination
@vaccination_bp.route('/<id>', methods=['GET'])
@jwt_required()
def get_vaccination(id):
    user_id = get_jwt_identity()
    vaccination = Vaccination.query.filter_by(id=id, user_id=user_id).first()
    
    if not vaccination:
        return jsonify({"message": "Vaccination not found"}), 404
    
    return jsonify(vaccination_schema.dump(vaccination)), 200

# POST /vaccinations - Add a new vaccination
@vaccination_bp.route('/add', methods=['POST'])
@jwt_required()
def add_vaccination():
    user_id = get_jwt_identity()
    data = request.get_json()
    
    # Validate data using the schema
    errors = vaccination_schema.validate(data)
    if errors:
        return jsonify(errors), 400
    
    # Check if the batch exists and belongs to the user
    batch = Batch.query.filter_by(id=data.get('batch_id'), user_id=user_id).first()
    if not batch:
        return jsonify({"message": "Batch not found or does not belong to you"}), 404
    
    vaccination = Vaccination(
        vaccine_name=data['vaccine_name'],
        description=data.get('description'),
        batch_id=batch.id,
        user_id=user_id
    )
    db.session.add(vaccination)
    db.session.commit()
    
    return jsonify(vaccination_schema.dump(vaccination)), 201

# PUT /vaccinations/<id> - Update an existing vaccination
@vaccination_bp.route('/<id>/update', methods=['PUT'])
@jwt_required()
def update_vaccination(id):
    user_id = get_jwt_identity()
    data = request.get_json()
    
    vaccination = Vaccination.query.filter_by(id=id, user_id=user_id).first()
    if not vaccination:
        return jsonify({"message": "Vaccination not found"}), 404
    
    # Update fields
    if 'vaccine_name' in data:
        vaccination.vaccine_name = data['vaccine_name']
    if 'description' in data:
        vaccination.description = data['description']
    
    db.session.commit()
    
    return jsonify(vaccination_schema.dump(vaccination)), 200

# DELETE /vaccinations/<id> - Delete a vaccination
@vaccination_bp.route('/<id>/delete', methods=['DELETE'])
@jwt_required()
def delete_vaccination(id):
    user_id = get_jwt_identity()
    vaccination = Vaccination.query.filter_by(id=id, user_id=user_id).first()
    
    if not vaccination:
        return jsonify({"message": "Vaccination not found"}), 404
    
    db.session.delete(vaccination)
    db.session.commit()
    
    return jsonify({"message": "Vaccination deleted successfully"}), 200