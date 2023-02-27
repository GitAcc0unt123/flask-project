from marshmallow import Schema, fields, validate

from src.models.tables.questions import AnswerTypeEnum

class QuestionSchema(Schema):
    id = fields.Integer(dump_only=True)
    test_id = fields.Integer(required=True, strict=True, validate=[validate.Range(min=1)])
    text = fields.Str(required=True, validate=validate.Length(min=1, max=255))
    answer_type = fields.Enum(AnswerTypeEnum, required=True)
    show_answers = fields.List(fields.Str(), required=True)
    true_answers = fields.List(fields.Str(), required=True)
