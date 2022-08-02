from django.db import models


class Campus(models.Model):
    """校区"""
    name = models.CharField(verbose_name="区域名", max_length=50, db_index=True, unique=True)
    client = models.GenericIPAddressField(help_text="区域IP")


class Building(models.Model):
    """宿舍楼"""
    name = models.CharField(verbose_name="宿舍楼名", max_length=50, db_index=True, unique=True)
    campus = models.ForeignKey(Campus, verbose_name="宿舍楼所在区域", on_delete=models.SET_NULL, null=True)
    szu_id = models.IntegerField(help_text="在深大系统中的id", db_index=True)


class Room(models.Model):
    campus = models.ForeignKey(Campus, verbose_name="宿舍所在区域", on_delete=models.SET_NULL, null=True)
    building = models.ForeignKey(Building, on_delete=models.SET_NULL, null=True)
    room_no = models.SmallIntegerField(verbose_name="宿舍房号", db_index=True)
    power_data = models.JSONField(verbose_name="电量记录", default=dict)
    szu_id = models.IntegerField(help_text="在深大系统中的id", default=0)

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['campus', 'building', 'room_no'], name='unique_room'),  # 唯一定位房间
        ]

    @property
    def building_szu_id(self):
        """宿舍所在楼ID"""
        return self.building.szu_id
