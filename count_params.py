#
# {'date': '17.11.2022',
#  'magnetic field': 'спокойное',
#  'periods': [{'condition': 'Дождь со снегом',
#               'humidity': '94%',
#               'period': 'Утром',
#               'pressure': '759',
#               'temp': {'max': '+1', 'min': '0'}},
#              {'condition': 'Дождь со снегом',
#               'humidity': '85%',
#               'period': 'Днём',
#               'pressure': '760',
#               'temp': {'max': '+1', 'min': '0'}},
#              {'condition': 'Дождь со снегом',
#               'humidity': '80%',
#               'period': 'Вечером',
#               'pressure': '763',
#               'temp': {'max': '0', 'min': '−1'}},
#              {'condition': 'Небольшой снег',
#               'humidity': '84%',
#               'period': 'Ночью',
#               'pressure': '764',
#               'temp': {'max': '−1', 'min': '−3'}}]}
import re


def pos_int(num):
    num = str(num.string)
    return int(num) if num[0] != '−' else -int(num[1:])


def light_avg_temp(day_list):
    avg_temp = sum(list(map(lambda x: (pos_int(x['temp']['max']) + pos_int(x['temp']['min'])) / 2, day_list[:3]))) / 3
    return avg_temp


def change_pressure(day_list: list) -> tuple:
    pressure = [int(prs['pressure']) for prs in day_list]
    min_prs = int(day_list[0]['pressure'])
    max_prs = int(day_list[0]['pressure'])
    direction = 0
    for day in day_list:
        pressure = int(day['pressure'])
        if pressure < min_prs:
            min_prs = pressure
            direction = -1
        elif pressure > max_prs:
            max_prs = pressure
            direction = 1
    return (max_prs - min_prs) >= 5, direction


if __name__ == '__main__':
    print()
