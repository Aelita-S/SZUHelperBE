from rest_framework import serializers
from rest_framework.exceptions import ValidationError

from power.models import Campus, Building, Room
from utils.data.dormitory import get_campus


class AreaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Campus
        fields = ('name',)
        read_only_fields = ('name',)


class BuildingSerializer(serializers.ModelSerializer):
    area = AreaSerializer()

    class Meta:
        model = Building
        fields = ('campus', 'name')
        read_only_fields = ('campus', 'name')


class RoomSerializer(serializers.ModelSerializer):
    building = BuildingSerializer()

    class Meta:
        model = Room
        exclude = ('campus',)
        read_only_fields = ('building', 'room_no', 'power_data')


class PowerInquirySerializer(serializers.Serializer):
    campusName = serializers.CharField(max_length=50, help_text="宿舍所在校区名")
    buildingID = serializers.IntegerField(help_text="宿舍楼ID")
    roomNo = serializers.IntegerField(help_text="宿舍房号")

    def validate_roomNo(self, value):
        try:
            assert 100 <= value <= 5000, "房号范围错误"
            return value
        except AssertionError as e:
            raise ValidationError(str(e))

    def validate_campusName(self, value):
        try:
            assert value in get_campus(), "区域错误"
            return value
        except AssertionError as e:
            raise ValidationError(str(e))

    def update(self, instance, validated_data):
        pass

    def create(self, validated_data):
        pass
