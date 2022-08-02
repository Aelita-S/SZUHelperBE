from datetime import datetime, timedelta

from pytz import timezone

loc_tz = timezone('Asia/Shanghai')


def loc2utc(dt: datetime) -> datetime:
    """将本地datetime对象转换为UTC时间对象"""
    return datetime.utcfromtimestamp(dt.timestamp())


def secs_left(hour: int = 0, minute: int = 0, second: int = 0) -> int:
    """离下一次到指定时间的秒数

    :param hour:
    :param minute:
    :param second:
    :return:
    """
    now = datetime.now(tz=loc_tz)
    next_datetime = datetime(now.year, now.month, now.day, hour, minute, second, tzinfo=now.tzinfo)
    if now.hour > hour and now.minute > minute and now.second > second:
        next_datetime += timedelta(days=1)
    rest_seconds = (next_datetime - now).seconds
    return rest_seconds


def secs_left_today() -> int:
    """返回今日剩余秒数"""
    return secs_left()


if __name__ == '__main__':
    print(secs_left(hour=19, minute=99, second=0), secs_left_today())
