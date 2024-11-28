from marshmallow import Schema, fields, validate

class ExpenseSchema(Schema):
    id = fields.String(dump_only=True)
    title = fields.String(required=True, validate=validate.Length(min=1))
    description = fields.String(allow_none=True)
    amount = fields.Float(required=True, validate=validate.Range(min=0))
    date_incurred = fields.DateTime(dump_only=True)
    batch_id = fields.String(allow_none=True)
    user_id = fields.String(dump_only=True)