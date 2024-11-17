from marshmallow import Schema, fields, validate

class FeedSchema(Schema):
    title = fields.String(required=True, validate=validate.Length(min=1))
    content = fields.String(required=True, validate=validate.Length(min=1))
    created_at = fields.DateTime(dump_only=True)