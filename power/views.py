from rest_framework.decorators import action
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet

from power.models import Room
from power.serializers import PowerInquirySerializer
from utils.power_inquiry import PowerUtil


class PowerViewSet(GenericViewSet):
    queryset = Room.objects.all()
    serializer_class = PowerInquirySerializer

    @action(methods=['post'], detail=False)
    def inquiry(self, request: Request, *args, **kwargs):
        """在线查询电量

        :param request:
        :return:
        """
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        campus_name: str = serializer.validated_data['campusName']
        building_id: int = serializer.validated_data['buildingID']
        room_no: int = serializer.validated_data['roomNo']

        power_data = PowerUtil(campus_name, building_id, room_no).inquiry()
        return Response(power_data)
