from marshmallow import Schema, fields, validate

class SignInSchema(Schema):
    username = fields.Str(required=True, validate=[
        validate.Regexp('^[A-Za-z]\w{2,254}$')])
    password = fields.Str(required=True, load_only=True, validate=[
        validate.Regexp('^[a-zA-Z0-9]{9,255}$')
    ])

class SignUpSchema(Schema):
    username = fields.Str(required=True, validate=[
        validate.Regexp('^[A-Za-z]\w{2,254}$')])
    password = fields.Str(required=True, load_only=True, validate=[
        validate.Regexp('^[a-zA-Z0-9]{9,255}$')
    ])
    name = fields.Str(required=True, validate=[
        validate.Length(min=1, max=255),
        validate.Regexp('^[a-zA-Z+ ]*[a-zA-Z]*$')
    ])
    email = fields.Email(required=True)
