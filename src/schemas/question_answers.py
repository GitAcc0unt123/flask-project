from marshmallow import Schema, fields, validate

class QuestionAnswerSchema(Schema):
    user_id = fields.Integer(dump_only=True)
    question_id = fields.Integer(required=True, strict=True, validate=[validate.Range(min=1)])
    answer = fields.List(fields.Str(), required=True)
    time = fields.DateTime(dump_only=True)
