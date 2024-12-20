from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from extensions import db
from models import Customer
from schemas.customer_schema import CustomerSchema

# Create Blueprint
customers_bp = Blueprint('customers', __name__)

# Initialize schema
customer_schema = CustomerSchema()
customers_schema = CustomerSchema(many=True)

# Routes
@customers_bp.route('/all', methods=['GET'])
@jwt_required()
def get_customers():
    user_id = get_jwt_identity()
    customers = Customer.query.filter_by(user_id=user_id).all()

    if not customers:
        return jsonify({"message": "No customers found"}), 404

    return jsonify(customers_schema.dump(customers)), 200


@customers_bp.route('/<id>', methods=['GET'])
@jwt_required()
def get_customer(id):
    user_id = get_jwt_identity()
    customer = Customer.query.filter_by(id=id, user_id=user_id).first()

    if not customer:
        return jsonify({"message": "Customer not found"}), 404

    return jsonify(customer_schema.dump(customer)), 200


@customers_bp.route('/add', methods=['POST'])
@jwt_required()
def add_customer():
    data = request.get_json()
    user_id = get_jwt_identity()

    # Validate the input using the schema
    errors = customer_schema.validate(data)
    if errors:
        return jsonify(errors), 400

    # Create a new customer with the provided data
    new_customer = Customer(
        name=data['name'],
        email=data.get('email'),
        phone=data['phone'],
        address=data.get('address'),
        user_id=user_id
    )
    db.session.add(new_customer)
    db.session.commit()

    # Serialize the newly created customer
    customer_data = customer_schema.dump(new_customer)
    return jsonify({"message": "Customer added successfully", "customer": customer_data}), 201



@customers_bp.route('/<id>', methods=['PUT'])
@jwt_required()
def update_customer(id):
    user_id = get_jwt_identity()
    customer = Customer.query.filter_by(id=id, user_id=user_id).first()

    if not customer:
        return jsonify({"message": "Customer not found"}), 404

    data = request.get_json()
    customer.name = data.get('name', customer.name)
    customer.email = data.get('email', customer.email)
    customer.phone = data.get('phone', customer.phone)
    customer.address = data.get('address', customer.address)

    db.session.commit()

    return jsonify(customer_schema.dump(customer)), 200


@customers_bp.route('/<id>', methods=['DELETE'])
@jwt_required()
def delete_customer(id):
    user_id = get_jwt_identity()
    customer = Customer.query.filter_by(id=id, user_id=user_id).first()

    if not customer:
        return jsonify({"message": "Customer not found"}), 404

    db.session.delete(customer)
    db.session.commit()

    return jsonify({"message": "Customer deleted successfully"}), 200
