from abc import ABCMeta, abstractmethod

from django.core.cache import cache

from utils.exceptions import SysOptionsException
from utils.time_utils import secs_left, secs_left_today


class CacheNotFoundError(KeyError):
    """缓存中未寻找到指定键"""
    pass


class BaseCache(metaclass=ABCMeta):
    """
    缓存抽象基类
    """
    KEY_PREFIX = None

    @classmethod
    def construct_key(cls, *args, **kwargs):
        pass

    @classmethod
    @abstractmethod
    def set(cls, *args, **kwargs) -> object:
        pass

    @classmethod
    @abstractmethod
    def get(cls, *args, **kwargs) -> object:
        pass


class ViewsCache(BaseCache):
    """访问数缓存，每日重置"""
    KEY_PREFIX = 'view'

    @classmethod
    def set(cls) -> int:
        """设置访问缓存"""
        cache.set(cls.KEY_PREFIX, 0, timeout=secs_left_today())
        return 0

    @classmethod
    def get(cls) -> int:
        """获取今日访问量

        :return: 今日访问量
        """
        if cls.KEY_PREFIX not in cache:
            return cls.set()
        return cache.get(cls.KEY_PREFIX)

    @classmethod
    def incr(cls) -> int:
        """访问数+1

        :return: 返回访问数
        """
        res = cls.get()
        cache.incr(cls.KEY_PREFIX)
        return res


class AccessTokenCache(BaseCache):
    """缓存微信AccessToken"""

    KEY_PREFIX = 'AccessToken'

    @classmethod
    def set(cls, token: str, expires_in: int) -> str:
        cache.set(cls.KEY_PREFIX, token, timeout=expires_in)
        return token

    @classmethod
    def get(cls):
        pass


class PowerCache(BaseCache):
    """电量缓存，记录今日已经查询过的宿舍及其电量信息"""
    KEY_PREFIX = 'Power{}{}{}'

    @classmethod
    def construct_key(cls, campus_name: str, building_id, room_no):
        return cls.KEY_PREFIX.format(campus_name, building_id, room_no)

    @classmethod
    def set(cls, campus_name: str, building_id, room_no, power_data):
        """

        :param campus_name: 宿舍所在校区名
        :param building_id: 宿舍所在楼ID
        :param room_no: 房间号
        :param power_data: 序列化的电量数据
        :return:
        """
        key = cls.construct_key(campus_name, building_id, room_no)
        cache.set(key, power_data, timeout=secs_left(hour=17, minute=55))

    @classmethod
    def get(cls, campus_name: str, building_id, room_no):
        """
        :param campus_name: 宿舍所在校区名
        :param building_id: 宿舍所在楼ID
        :param room_no: 房间号
        """
        key = cls.construct_key(campus_name, building_id, room_no)
        if key in cache:
            return cache.get(key)
        else:
            raise CacheNotFoundError


class SysOptionsCache(BaseCache):
    KEY_PREFIX = 'Sysoptions:{}'

    @classmethod
    def construct_key(cls, option_key: str):
        return cls.KEY_PREFIX.format(option_key)

    @classmethod
    def set(cls, option_key: str, value):
        """系统设置缓存15分钟

        :param option_key:
        :param value:
        :return:
        """
        cache_key = cls.construct_key(option_key)
        cache.set(cache_key, value, timeout=15 * 60)
        return value

    @classmethod
    def get(cls, option_key: str):
        cache_key = cls.construct_key(option_key)
        if cache_key in cache:
            return cache.get(cache_key)
        else:
            from sysoptions.models import SysOptions
            try:
                value = SysOptions.objects.get(key=option_key).value
                return cls.set(cache_key, value)
            except SysOptions.DoesNotExist:
                raise SysOptionsException()
