from django.db import models

from utils.base_models import BaseInfoModel


class Document(BaseInfoModel):
    department = models.CharField(verbose_name="部门名", max_length=100, db_index=True)
    doc_id = models.PositiveIntegerField(verbose_name="公文通id", db_index=True, unique=True, default=0)
    category = models.CharField(verbose_name="类别", max_length=20, default="", db_index=True)

    class Meta:
        ordering = ('-last_update_time',)
