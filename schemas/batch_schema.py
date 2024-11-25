from marshmallow import Schema, fields, validate

class BatchSchema(Schema):
    id = fields.String(dump_only=True)
    name = fields.String(required=True, validate=validate.Length(min=1))
    start_date = fields.DateTime(dump_only=True)
    end_date = fields.DateTime(allow_none=True)
    quantity = fields.Integer(required=True)
    status = fields.String(dump_only=True)
    mortality = fields.Integer(required=True, validate=validate.Range(min=0))  # Ensure non-negative values
    feed_id = fields.String(allow_none=True)
    user_id = fields.String(dump_only=True)
    batch_number = fields.String(dump_only=True)
