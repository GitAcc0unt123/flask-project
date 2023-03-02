from marshmallow import Schema, fields, validate, validates_schema, ValidationError

from src.models.tables import AnswerTypeEnum


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


    answer_type = fields.Enum(AnswerTypeEnum, required=True, load_only=True)
    question_show_answers = fields.List(
        fields.Str(required=True, validate=[validate.Length(min=1)]),
        required=True,
        load_only=True
    )

    @validates_schema()
    def validate_answer(self, data, **kwargs):
        answer_fields = ['answer', 'answer_type', 'question_show_answers']

        if any(field not in data for field in answer_fields):
            raise ValidationError(['Required fields: answer, answer_type, question_show_answers'])

        if data['answer_type'] is AnswerTypeEnum.free_field:
            if len(data['answer']) != 1:
                raise ValidationError('', 'answer')
        elif data['answer_type'] is AnswerTypeEnum.one_select:
            if len(data['answer']) != 1 or data['answer'][0] not in data['question_show_answers']:
                raise ValidationError('', 'answer')
        elif data['answer_type'] is AnswerTypeEnum.many_select:
            if len(data['answer']) < 1 or data['answer'][0] not in data['question_show_answers']:
                raise ValidationError('', 'answer')
