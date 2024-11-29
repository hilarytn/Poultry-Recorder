from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from marshmallow import ValidationError
from extensions import db
from models.expense import Expense
from schemas.expense_schema import ExpenseSchema

expenses_bp = Blueprint('expenses', __name__)
expense_schema = ExpenseSchema()
expenses_schema = ExpenseSchema(many=True)

# GET /expense - Retrieve all expenses (general and batch-specific)
@expenses_bp.route('/all', methods=['GET'])
@jwt_required()
def get_expenses():
    user_id = get_jwt_identity()
    expenses = Expense.query.filter_by(user_id=user_id).all()
    if not expenses:
        return jsonify({"message": "No expenses yet"}), 404
    return jsonify(expenses_schema.dump(expenses)), 200

# GET /expense/<id> - Retrieve details for a specific expense
@expenses_bp.route('/<id>', methods=['GET'])
@jwt_required()
def get_expense(id):
    user_id = get_jwt_identity()
    expense = Expense.query.filter_by(id=id, user_id=user_id).first()
    if not expense:
        return jsonify({"message": "Expense not found"}), 404
    return jsonify(expense_schema.dump(expense)), 200

# POST /expenses - Add a new expense
@expenses_bp.route('/add', methods=['POST'])
@jwt_required()
def create_expense():
    user_id = get_jwt_identity()
    data = request.get_json()

    try:
        expense = expense_schema.load(data)
    except ValidationError as err:
        return jsonify(err.messages), 400

    new_expense = Expense(
        title=expense['title'],
        description=expense.get('description'),
        amount=expense['amount'],
        batch_id=expense.get('batch_id'),
        user_id=user_id
    )
    db.session.add(new_expense)
    db.session.commit()
    return jsonify(expense_schema.dump(new_expense)), 201

# PUT /expenses/<id> - Update an existing expense
@expenses_bp.route('/expenses/<id>', methods=['PUT'])
@jwt_required()
def update_expense(id):
    user_id = get_jwt_identity()
    expense = Expense.query.filter_by(id=id, user_id=user_id).first()
    if not expense:
        return jsonify({"message": "Expense not found"}), 404

    data = request.get_json()
    try:
        updated_data = expense_schema.load(data, partial=True)
    except ValidationError as err:
        return jsonify(err.messages), 400

    expense.title = updated_data.get('title', expense.title)
    expense.description = updated_data.get('description', expense.description)
    expense.amount = updated_data.get('amount', expense.amount)
    expense.batch_id = updated_data.get('batch_id', expense.batch_id)
    db.session.commit()
    return jsonify(expense_schema.dump(expense)), 200

# DELETE /expenses/<id> - Delete an expense
@expenses_bp.route('/expenses/<id>', methods=['DELETE'])
@jwt_required()
def delete_expense(id):
    user_id = get_jwt_identity()
    expense = Expense.query.filter_by(id=id, user_id=user_id).first()
    if not expense:
        return jsonify({"message": "Expense not found"}), 404

    db.session.delete(expense)
    db.session.commit()
    return jsonify({"message": "Expense deleted successfully"}), 200
