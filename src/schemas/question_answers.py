from marshmallow import Schema, fields, validate


class QuestionAnswerSchema(Schema):
    user_id = fields.Integer()
    question_id = fields.Integer(required=True, strict=True, validate=[validate.Range(min=1)])
    answer = fields.List(
        fields.Str(required=True, validate=[validate.Length(min=1)]),
        required=True,
        validate=[validate.Length(min=1)]
    )
    time = fields.DateTime()

    class Meta:
        dump_only = ['user_id', 'time']
