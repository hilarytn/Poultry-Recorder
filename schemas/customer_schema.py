from marshmallow import Schema, fields, validate

class CustomerSchema(Schema):
    id = fields.String(dump_only=True)
    name = fields.String(required=True, validate=validate.Length(min=1))
    email = fields.Email(allow_none=True)
    phone = fields.String(required=True, validate=validate.Length(min=10, max=20))
    address = fields.String(allow_none=True)
    user_id = fields.String(dump_only=True)