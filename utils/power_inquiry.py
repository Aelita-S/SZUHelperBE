import os
from datetime import datetime, timedelta
from re import findall
from typing import List

import requests
from django.conf import settings
from lxml import etree
from requests import get
from rest_framework.status import is_success

from power.models import Campus, Building, Room
from utils.cache import CacheNotFoundError, PowerCache
from utils.data.dormitory import get_client
from utils.exceptions import PowerInquiryException
from utils.user_agent import rand_UA

login_url = 'http://192.168.84.3:9090/cgcSims/login.do'
get_info_url = 'http://192.168.84.3:9090/cgcSims/selectList.do'

PROXY = os.getenv('PROXY', '127.0.0.1:8118')


def get_or_create_room(campus_name: str, building_id: int, room_no: int) -> (Room, bool):
    """根据 区域名、楼栋ID 获得或者创建宿舍对象

    :param campus_name: 校区名
    :param building_id: 楼栋ID
    :param room_no: 房间号
    :return:
    """
    campus = Campus.objects.get(name=campus_name)
    building = Building.objects.get(campus=campus, szu_id=building_id)
    return Room.objects.get_or_create(campus=campus, building=building, room_no=room_no)


class PowerUtil:
    """查询电量信息工具类"""

    def __init__(self, campus_name: str, building_id: int, room_no: int):
        """

        :param campus_name: 校区名
        :param building_id: 宿舍楼栋ID
        :param room_no: 房号
        """
        self.campus_name = campus_name
        self.building_id = building_id
        self.room_no = room_no
        self.proxies = {
            'http': f'http://{PROXY}', 'https': f'https://{PROXY}',
        } if not settings.DEBUG else {}
        self.session = requests.session()
        self.room, self.created = get_or_create_room(campus_name, building_id, room_no)

    def inquiry(self) -> List[dict]:
        """查询宿舍电量信息，保存至缓存、数据库，并返回

        :return: [
                    {
                        "date": "2020-10-15",
                        "remain": 158.2,
                        "usage": 16641.11
                    },
                ]
        """
        if self.created:
            self.room.szu_id = self.get_room_id()
        try:  # 查询是否在缓存中
            power_data = PowerCache.get(self.campus_name, self.building_id, self.room_no)
        except CacheNotFoundError:  # 不在缓存中则说明需要重新获取
            detail_data = self._fill_detail_data()
            detail_raw = self.session.post(url=get_info_url, data=detail_data, headers=rand_UA, proxies=self.proxies)
            assert is_success(detail_raw.status_code) is True, \
                f"请求失败：{self.campus_name} Building_ID: {self.building_id} Room_No: {self.room_no}"
            detail_html = etree.HTML(detail_raw.text)

            power_data = self._parse_power_detail(detail_html)

            self.room.power_data = power_data
            self.room.save()

            PowerCache.set(self.campus_name, self.building_id, self.room_no, power_data)
        return power_data

    def get_room_id(self) -> int:
        """获得房间在深大系统中的ID

        :return:
        """
        room_data = self._fill_room_data()

        req = self.session.post(url=login_url, data=room_data, headers=rand_UA, proxies=self.proxies)
        assert is_success(req.status_code) is True, "请求失败"
        html = etree.HTML(req.text)

        try:
            room_id: str = html.xpath('//input[@name="roomId"]/@value')[0]
        except IndexError:  # 只有存在的房间才继续查询
            self.room.delete()  # 不存在则删除该房间
            raise PowerInquiryException(
                f"Campus:{self.campus_name} Building_id: {self.building_id} Room_no: {self.room_no}")
        return int(room_id)

    def _fill_room_data(self):
        """填充房间信息

        :return:
        """
        client = get_client(self.campus_name)
        room_data = {
            'client': client,
            'buildingName': '',
            'buildingId': self.building_id,
            'roomName': str(self.room_no),
            'select': '',
        }
        return room_data

    def _fill_detail_data(self):
        """填充查询请求信息

        :return:
        """
        campus_name = self.campus_name

        client = get_client(campus_name)
        now = datetime.now()

        begin_time = datetime.strftime(now - timedelta(days=14), '%Y-%m-%d')  # 查询14天以内的信息
        end_time = datetime.strftime(now, '%Y-%m-%d')

        detail_data = {
            'hiddenType': '',
            'isHost': '0',
            'beginTime': begin_time,
            'endTime': end_time,
            'type': '2',
            'client': client,
            'roomId': str(self.room.szu_id),
            'roomName': str(self.room_no) + '                 ',
            'building': '',
        }
        return detail_data

    def _parse_power_detail(self, html: etree.HTML):
        """xpath分析宿舍电量网页

        :param html:
        :return:
        """

        def parse_date(line) -> str:
            """从一行字符串中提取日期"""
            date_str = findall(r'\d{4}-\d{2}-\d{2}', line)[0]
            return date_str

        def generate_power_detail_obj(update_date: str, remain: float, usage: float) -> dict:
            """生成每日电量详情字典"""
            return dict(date=update_date, remain=remain, usage=usage)

        remain_list_raw = html.xpath('//*[@id="oTable"]//tr[position()>1]/td[3]//text()')
        usage_list_raw = html.xpath('//*[@id="oTable"]//tr[position()>1]/td[4]//text()')
        datetime_list_raw = html.xpath('//*[@id="oTable"]//tr[position()>1]/td[6]//text()')

        remain_list = [float(x) for x in remain_list_raw]
        usage_list = [float(x) for x in usage_list_raw]
        date_list = [parse_date(line) for line in datetime_list_raw]

        power_list: list = [generate_power_detail_obj(d, r, u) for d, r, u in zip(date_list, remain_list, usage_list)]
        # power_data = {date: power for date, power in zip(datetime_list, quantity_list)}
        return power_list

    @staticmethod
    def get_area():
        area_dict_list = {}

        req = get(login_url, headers=rand_UA)
        if req.status_code != 200:
            print("Error!")
            exit(0)

        # print(req.text)
        html = etree.HTML(req.text)
        area_list = html.xpath('//*[@onchange="changeBuilding(this.value)"]//option//text()')
        area_url_list = html.xpath('//*[@onchange="changeBuilding(this.value)"]//option//@value')
        for (area, url) in zip(area_list, area_url_list):
            area_dict_list.update({area: {'client': url}})
        return area_dict_list

    @staticmethod
    def get_building_list(area_client: str):
        # print(login_url + area_client)
        url = login_url + "?task=station&client=" + area_client
        print(url)
        req = get(url, headers=rand_UA)
        if req.status_code != 200:
            print("Error!")
            exit(0)

        html = etree.HTML(req.text)
        building_list_raw_text = html.xpath(
            """//*[@onchange="document.getElementById('buildingName')."""
            """value=this.options[this.selectedIndex].text"]//option[@value]//text()""")
        # print(building_list_raw_text)
        building_id_list = html.xpath(
            """//*[@onchange="document.getElementById('buildingName')."""
            """value=this.options[this.selectedIndex].text"]//option[@value]//@value""")
        building_dict = {}
        building_id_list.remove(building_id_list[0])
        building_list_raw_text.remove(building_list_raw_text[0])
        for (building_id, building_name) in zip(building_id_list, building_list_raw_text):
            building_dict.update({int(building_id): str(building_name).strip()})
        # print(building_dict)
        return building_dict


if __name__ == '__main__':
    # campus = get_area()
    # print(campus)
    # for client in campus.values():
    #     print(get_building_list(client['client']))

    # print(inquiry('北校区', 6878, 1917))
    print(PowerUtil('北校区', 6877, 1917).get_room_id())
