from flask import Blueprint, jsonify, request
from extensions import db
from models.sale import Sale
from models.batch import Batch
from schemas.sale_schema import SaleSchema
from flask_jwt_extended import jwt_required, get_jwt_identity

sales_bp = Blueprint('sales', __name__)


sale_schema = SaleSchema()
sales_schema = SaleSchema(many=True)

@sales_bp.route('/sales', methods=['POST'])
@jwt_required()
def add_sale():
    data = request.get_json()
    user_id = get_jwt_identity()

    # Validate the input using the schema
    errors = sale_schema.validate(data)
    if errors:
        return jsonify(errors), 400

    # Check if batch exists for the sale, if `batch_id` is provided
    batch = None
    if 'batch_id' in data and data['batch_id']:
        batch = Batch.query.filter_by(id=data['batch_id'], user_id=user_id).first()
        if not batch:
            return jsonify({"message": "Batch not found or not associated with the user"}), 404

    # Create a new sale with the provided data
    new_sale = Sale(
        item=data['item'],
        quantity=data['quantity'],
        price=data['price'],
        total_amount=data['quantity'] * data['price'], 
        sale_date=data.get('sale_date'),
        batch_id=data.get('batch_id'), 
        user_id=user_id
    )
    db.session.add(new_sale)
    db.session.commit()

    # Serialize the newly created sale
    sale_data = sale_schema.dump(new_sale)
    return jsonify({"message": "Sale added successfully", "sale": sale_data}), 201

@sales_bp.route('/all', methods=['GET'])
@jwt_required()
def get_sales():
    user_id = get_jwt_identity() 
    sales = Sale.query.filter_by(user_id=user_id).all()

    if not sales:
        return jsonify({"message": "No sales found"}), 404

    sales_data = sales_schema.dump(sales, many=True)
    return jsonify({"sales": sales_data}), 200
