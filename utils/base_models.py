import logging

from django.db import models
from lxml.etree import ParserError
from lxml.html.clean import clean_html

from utils.validators import JSONValidator

logger = logging.getLogger(__name__)


class RichTextField(models.TextField):
    """XSS过滤"""

    def pre_save(self, model_instance, add):
        """将字符串保存到数据库前过滤"""
        value = super().pre_save(model_instance, add)
        if value is not None and value != "" and not self.null:
            try:
                value = clean_html(value)
            except ParserError as e:
                logger.error(msg='Error value: ' + value)
        return value


class BaseInfoModel(models.Model):
    """
    信息基类，子类可以是文章，项目……
    默认以id逆序排序
    """
    title = models.CharField(verbose_name="标题", max_length=100)
    # 外键，创建者; SET_NULL表示对应用户被删除时置空
    create_time = models.DateTimeField(verbose_name="创建时间")
    last_update_time = models.DateTimeField(verbose_name="上次更新时间")
    content = RichTextField()  # XSS过滤

    class Meta:
        abstract = True

    def __str__(self):
        return self.title


class JSONSchemaField(models.JSONField):
    def __init__(self, schema: dict = None, *args, **kwargs):
        self.schema = schema
        self.validator = JSONValidator(self.schema)
        super().__init__(*args, **kwargs)

    def _validate_schema(self, value):
        if self.model.__module__ == '__fake__':
            return True
        self.validator.validate(value)

    def validate(self, value, model_instance):
        super().validate(value, model_instance)
        self._validate_schema(value)

    def pre_save(self, model_instance, add):
        value = super().pre_save(model_instance, add)
        if value and not self.null:
            self._validate_schema(value)
        return value
