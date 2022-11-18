from load_to_db import load_result_to_db
from parser_weather import parsing_weather
from put_to_excel import write_to_excel

import argparse
def parse_arg():
    parser = argparse.ArgumentParser(description='Videos to images')
    parser.add_argument('--city', '-c', type=str, help='Input name of city')
    args = parser.parse_args()
    return args.city


if __name__ == "__main__":
    city = parse_arg()
    # city = input()
    try:
        weather = parsing_weather(city)
    except:
        load_result_to_db(city, error='Ошибка')
        print('Возникла ошибка. Файл не сформирован')
    else:
        load_result_to_db(city)
        write_to_excel(weather, city)
        print('Файл (Weather.xlsx) сформирован')
