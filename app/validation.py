from marshmallow import Schema, fields, validates_schema, ValidationError

class RegisterSchema(Schema):
    username = fields.Str(required=True)
    password = fields.Str(required=True)

class LoginSchema(Schema):
    username = fields.Str(required=True)
    password = fields.Str(required=True)

class GenerateTextSchema(Schema):
    prompt = fields.Str(required=True)