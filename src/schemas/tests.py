from marshmallow import Schema, fields, validate, validates, ValidationError, post_load

class TestSchema(Schema):
    id = fields.Integer(dump_only=True)
    title = fields.Str(required=True, validate=validate.Length(min=3, max=255)) # error_messages={"required": {"message": "City required", "code": 400}}
    description = fields.Str(required=False, validate=validate.Length(min=1, max=255))
    start = fields.DateTime(required=True)
    end = fields.DateTime(required=True)

    class Meta:
        ordered = True

    # @validates("end")
    # def validate_end(self, value):
    #     if value <= self.start: # остальные поля не проинициализированы
    #         raise ValidationError("end <= start")

    # по умолчанию возвращает словать с десериализованными и проверенными полями
    # можно возвращать сразу объект. при создании объекта могут быть новые исключения
    # @post_load
    # def make_user(self, data, **kwargs):
    #     return User(**data)