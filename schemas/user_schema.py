from marshmallow import Schema, fields, validate

class UserSchema(Schema):
    fullname = fields.String(required=True, validate=validate.Length(min=2))
    username = fields.String(required=True, validate=validate.Length(min=2))
    email = fields.Email(required=True)
    password = fields.String(required=True, validate=validate.Regexp(
        r'^(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*#?&])[A-Za-z\d@$!%*#?&]{8,}$',
        error="Password must have at least 8 characters, one uppercase, one number, and one special character."
    ))