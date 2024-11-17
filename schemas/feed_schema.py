from marshmallow import Schema, fields, validate

class FeedSchema(Schema):
    name = fields.String(required=True, validate=validate.Length(min=1))
    description = fields.String(allow_none=True)
    quantity = fields.Float(required=True)
