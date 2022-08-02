campus = {'北校区': {'client': '192.168.84.1',
                  'buildings': {6121: '乔林阁1-10楼', 6122: '乔木阁1-10楼', 6363: '乔林阁11-12', 6364: '乔木阁11-12',
                                7724: '乔梧阁2-10层', 7725: '乔梧阁11-20', 6875: '乔森阁2-10层', 6876: '乔森11-20层',
                                6877: '乔相阁2-10层', 6878: '乔相11-20层', 8147: '留学生公寓', 50: '木棉斋', 51: '拒霜斋', 54: '山茶斋',
                                55: '红榴斋', 56: '米兰斋', 57: '海桐斋', 58: '桃李斋', 59: '凌霄斋', 61: '银桦斋', 63: '木犀轩',
                                64: '丹枫轩', 65: '紫檀轩', 66: '石楠轩', 67: '苏铁轩', 68: '芸香阁', 69: '丁香阁', 70: '文杏阁',
                                71: '海棠阁', 72: '疏影阁', 73: '杜衡阁', 74: '辛夷阁', 75: '韵竹阁', 76: '云杉轩', 77: '紫藤轩'}
                  },
          '南校区': {'client': '192.168.84.228',
                  'buildings': {8241: '冬筑11-14楼', 6875: '春笛3-8楼', 6876: '夏筝3-17楼', 6877: '秋瑟3-8楼', 6878: '冬筑3-6楼',
                                7119: '春笛9-17楼', 7828: '秋瑟9-17楼', 8240: '冬筑7-10楼', 8242: '冬筑15-17楼'}
                  },
          '西丽校区': {'client': '172.21.101.11',
                   'buildings': {10057: 'A栋风信子',
                                 10934: 'B栋山楂树',
                                 10935: 'C栋胡杨林'}},
          '深大新斋区': {'client': '192.168.84.87',
                    'buildings': {7126: '风槐斋', 7603: '雨鹃斋', 17887: '蓬莱客舍',
                                  18118: '聚翰斋', 18119: '紫薇斋', 18120: '红豆斋'}
                    }
          }


def get_campus():
    return campus.keys()


def get_client(campus_name: str):
    """通过区域名获取client"""
    return campus[campus_name]['client']


def get_building_name(campus_name: str, building_id: int):
    """

    :param campus_name: 区域名
    :param building_id: 建筑id
    :return: 建筑名
    """
    return campus[campus_name]['buildings'][building_id]


def main():
    from power.models import Campus, Building

    for campus_name, area_data in campus.items():
        client = area_data['client']
        area = Campus(name=campus_name, client=client)
        area.save()
        for building_id, building_name in area_data['buildings'].items():
            Building(area=area, szu_id=building_id, name=building_name).save()


if __name__ == '__main__':
    print(get_campus())
