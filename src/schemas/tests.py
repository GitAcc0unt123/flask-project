from marshmallow import Schema, fields, validate, validates, ValidationError, post_load

class TestSchema(Schema):
    id = fields.Integer(dump_only=True)
    title = fields.Str(required=True, validate=validate.Length(min=3, max=255))
    description = fields.Str(required=False, validate=validate.Length(min=1, max=255))
    start = fields.DateTime(required=True)
    end = fields.DateTime(required=True)

    class Meta:
        ordered = True
