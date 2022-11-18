import datetime
from pprint import pprint

from selenium import webdriver
from selenium.webdriver import Keys
from selenium.webdriver.chrome.webdriver import WebDriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup

from load_to_db import city_coordinate


def init_driver() -> WebDriver:
    from fake_useragent import UserAgent
    ua = UserAgent()
    agent = ua.random
    options = Options()

    service = Service()
    options.add_argument("--headless")
    options.add_argument(f'user-agent={agent}')
    driver = webdriver.Chrome(options=options, service=service)
    return driver


def get_coordinates(city: str, driver: WebDriver) -> list:
    driver.get('https://time-in.ru/coordinates/')
    input_city = driver.find_element(by=By.CLASS_NAME, value='ui-autocomplete-input')
    input_city.send_keys(city)
    input_city.send_keys(Keys.RETURN)
    coordinates = driver.find_element(by=By.CLASS_NAME, value='coordinates-city-info').find_element(by=By.TAG_NAME,
                                                                                                    value="div").text
    coordinates = coordinates.split(': ')[1]
    return coordinates.split(', ')


def parsing_weather(city):
    driver = init_driver()
    coordinates = city_coordinate(city)

    weather = []

    url = f'https://yandex.ru/pogoda/?lat={coordinates[0]}&lon={coordinates[1]}&via=srp'
    driver.get(url)
    link_to_articles = driver.find_element(by=By.XPATH,
                                           value='//div[contains(@class, "forecast-briefly__days")]').find_element(
        by=By.TAG_NAME, value='ul').find_element(by=By.XPATH,
                                                 value='.//li[contains(@class, "swiper-slide-next")]//a').get_attribute(
        'href')
    driver.get(link_to_articles)
    WebDriverWait(driver, 30).until(EC.presence_of_element_located((By.XPATH, '//article[@class="card"]')))

    html = driver.page_source
    soup = BeautifulSoup(html, 'html.parser')
    driver.quit()

    articles = soup.find_all("article", class_='card')
    month = datetime.date.today().month
    year = datetime.date.today().year
    for article in articles:
        day = {'periods': []}
        try:
            div_date = article.find_all(attrs={'data-anchor': True})[0].get('data-anchor')
        except IndexError:
            continue

        day['date'] = f'{div_date.split("_")[1]}.{month}.{year}'
        div_table = article.find('tbody').find_all('tr')
        for tr in div_table:
            period = tr.find('td', class_='weather-table__body-cell_type_daypart').find('span').find("div")
            temp_dict = {'temp': {}}
            temp_dict['period'] = period.find(class_="weather-table__daypart").string
            temp = period.find_all("span")
            # temp = temp.find("div", class_='weather-table__wrapper')
            # temp = temp.find("div", class_='weather-table__temp').find_all('div', class_='temp')
            if len(temp) > 1:
                temp_dict['temp']['min'] = temp[0].contents[0]
                temp_dict['temp']['max'] = temp[1].contents[0]
            else:
                temp_dict['temp']['min'] = temp[0].contents[0]
                temp_dict['temp']['max'] = temp[0].contents[0]
            temp_dict['pressure'] = tr.find('td', class_='weather-table__body-cell_type_air-pressure').string
            temp_dict['humidity'] = tr.find('td', class_='weather-table__body-cell_type_humidity').string
            temp_dict['condition'] = tr.find('td', class_='weather-table__body-cell_type_condition').string
            day['periods'].append(temp_dict)
        magnetic = article.find_all('dd', class_="forecast-fields__value")
        if len(magnetic) > 1:
            day['magnetic field'] = magnetic[-1].string
        else:
            day['magnetic field'] = 'N/D'

        weather.append(day)
        if len(weather) == 7:
            break

    return weather


if __name__ == '__main__':
    city = input()
    pprint(parsing_weather(city))
