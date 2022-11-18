from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from fake_useragent import UserAgent


def get_coordinates(city):
    ua = UserAgent()
    agent = ua.random
    options = Options()
    options.add_argument(f'user-agent={agent}')
    options.add_argument("--headless")

    driver = webdriver.Chrome(options=options)

    driver.get('https://time-in.ru/coordinates/')
    input_city = driver.find_element(by=By.CLASS_NAME, value='ui-autocomplete-input')
    input_city.send_keys(city)
    input_city.send_keys(Keys.RETURN)

    coordinates = driver.find_element(by=By.CLASS_NAME, value='coordinates-city-info').find_element(by=By.TAG_NAME,
                                                                                                  value="div").text

    coordinates = coordinates.split(': ')[1]
    return coordinates.split(', ')
