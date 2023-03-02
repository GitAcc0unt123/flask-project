from marshmallow import Schema, fields, validate, validates_schema, ValidationError

from src.models.tables.questions import AnswerTypeEnum


class QuestionSchema(Schema):
    id = fields.Integer(dump_only=True)
    test_id = fields.Integer(required=True, strict=True, validate=[validate.Range(min=1)])
    text = fields.Str(required=True, validate=validate.Length(min=1, max=255))
    answer_type = fields.Enum(AnswerTypeEnum, required=True)

    show_answers = fields.List(
        fields.Str(required=True, validate=[validate.Length(min=1)]),
        required=True)

    true_answers = fields.List(
        fields.Str(required=True, validate=[validate.Length(min=1)]),
        required=True,
        validate=[validate.Length(min=1)])


    @validates_schema()
    def validate_answer(self, data, **kwargs):
        if all(field in data for field in ('answer_type', 'show_answers', 'true_answers')):
            answer_type = data['answer_type']
            show_answers_len = len(data['show_answers'])
            true_answers_len = len(data['true_answers'])

            if answer_type == AnswerTypeEnum.free_field:
                if show_answers_len > 0:
                    raise ValidationError('Value should be an empty list', 'show_answers')
                elif true_answers_len != 1:
                    raise ValidationError('Value should be a list with one element', 'true_answers')

            elif answer_type == AnswerTypeEnum.one_select:
                if show_answers_len <= 1:
                    raise ValidationError('Value should be a list with at least two elements', 'show_answers')
                elif true_answers_len != 1:
                    raise ValidationError('Value should be a list with one element', 'true_answers')
                elif data['true_answers'][0] not in data['show_answers']:
                    raise ValidationError('True answer must be in show answers', 'true_answers')

            elif answer_type == AnswerTypeEnum.many_select:
                if show_answers_len <= 1:
                    raise ValidationError('Value should be a list with at least two elements', 'show_answers')
                elif true_answers_len < 1:
                    raise ValidationError('Value should be a list with at least one element', 'true_answers')
                elif not (set(data['true_answers']).issubset( set(data['show_answers']) )):
                    raise ValidationError('True answers must be in show answers', 'true_answers')

        elif any(field in data for field in ('answer_type', 'show_answers', 'true_answers')):
            raise ValidationError(
                    'Required fields: answer_type, show_answers, true_answers',
                )
