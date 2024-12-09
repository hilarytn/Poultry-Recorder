from marshmallow import Schema, fields, validate

class SaleSchema(Schema):
    id = fields.String(dump_only=True)
    item_name = fields.String(required=True, validate=validate.Length(min=1))
    quantity = fields.Integer(required=True, validate=validate.Range(min=1))
    price_per_unit = fields.Float(required=True, validate=validate.Range(min=0))
    total_price = fields.Float(dump_only=True)
    date = fields.DateTime(dump_only=True) 
    user_id = fields.String(dump_only=True)
    batch_id = fields.String(allow_none=True)