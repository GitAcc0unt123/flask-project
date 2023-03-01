from marshmallow import Schema, fields, validate, validates_schema, ValidationError


class TestSchema(Schema):
    id = fields.Integer(dump_only=True)
    title = fields.Str(required=True, validate=validate.Length(min=3, max=255))
    description = fields.Str(required=False, validate=validate.Length(min=1, max=255))
    start = fields.DateTime(required=True)
    end = fields.DateTime(required=True)

    class Meta:
        ordered = True

    @validates_schema()
    def validate_time(self, data, **kwargs):
        if 'start' not in data and 'end' in data:
            raise ValidationError(
                    'Missing data for required field.',
                    'start'
                )
        elif 'start' in data and 'end' not in data:
            raise ValidationError(
                    'Missing data for required field.',
                    'end'
                )
        elif 'start' in data and 'end' in data and data['end'] <= data['start']:
            raise ValidationError(
                'End time should be after start time.',
                'end'
            )
