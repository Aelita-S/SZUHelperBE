import fastjsonschema
from django.utils.deconstruct import deconstructible
from fastjsonschema import JsonSchemaException
from rest_framework.exceptions import ValidationError


@deconstructible
class JSONValidator:
    """传入JSON schema，生成对应schema的校验器"""

    def __init__(self, schema: dict):
        """

        :param schema: JSON schema
        """
        self.schema = schema

    def __call__(self, value: dict):
        self.validate(value)

    def validate(self, value: dict) -> dict:
        """校验JSON是否与schema一致"""
        if self.schema is None:
            return value
        try:
            fastjsonschema.validate(definition=self.schema, data=value)
        except JsonSchemaException as e:
            raise ValidationError(detail=str(e))
        return value
