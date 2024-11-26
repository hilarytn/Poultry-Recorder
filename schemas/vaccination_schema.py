from marshmallow import Schema, fields, validate

class VaccinationSchema(Schema):
    id = fields.String(dump_only=True)
    vaccine_name = fields.String(required=True, validate=validate.Length(min=1))
    date = fields.DateTime(dump_only=True)
    description = fields.String(allow_none=True, validate=validate.Length(max=255))
    batch_id = fields.String(required=True)
    user_id = fields.String(dump_only=True)