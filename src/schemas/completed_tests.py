from marshmallow import Schema, fields, validate


class CompletedTestSchema(Schema):
    user_id = fields.Integer(required=True, strict=True, validate=[validate.Range(min=1)])
    test_id = fields.Integer(required=True, strict=True, validate=[validate.Range(min=1)])
    complete_time = fields.DateTime(dump_only=True)
