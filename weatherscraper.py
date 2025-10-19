import re
import json
from datetime import date
from typing import List, Tuple, Union
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup
from tabulate import tabulate


def get_forecast_data():
    """
    Fetch weather forecast data from world-weather.info.

    Returns:
        List of tuples: [(city, temperature, condition), ...]
        or a message string if data is not found.
    """
    options = Options()
    options.add_argument('--headless')
    options.add_argument('--disable-gpu')
    options.add_argument('--no-sandbox')
    options.add_argument('--log-level=3')

    # Disable images, plugins, popups, notifications, media_stream
    prefs = {
        "profile.default_content_setting_values": {
            "images": 2,
            "plugins": 2,
            "popups": 2,
            "notifications": 2,
            "media_stream": 2,
        }
    }
    options.add_experimental_option("prefs", prefs)

    driver = webdriver.Chrome(options=options)

    try:
        driver.get("https://world-weather.info/")
        driver.add_cookie({"name": "celsius", "value": "1"})
        driver.refresh()

        html = driver.page_source
        soup = BeautifulSoup(html, "html.parser")
        resorts = soup.find("div", id="resorts")

        if not resorts:
            return "No forecast data found."

        # Extract cities
        re_cities = r'">([\w\s]+)</a><span>'
        cities = re.findall(re_cities, str(resorts))

        # Extract temperatures
        re_temps = r'<span>(\+\d+|-\d+)<span'
        temps = [int(temp) for temp in re.findall(re_temps, str(resorts))]

        # Extract conditions
        conditions_tags = resorts.find_all('span', class_='tooltip')
        conditions = [tag.get('title') for tag in conditions_tags]

        data = list(zip(cities, temps, conditions))

        return data if data else "No forecast data found."

    finally:
        driver.quit()


def get_forecast_txt():
    """
    Save weather data to a text file (output.txt) with a formatted table.
    """
    data = get_forecast_data()
    if not isinstance(data, list):
        print(data)
        return

    today = date.today().strftime('%d/%m/%Y')
    with open('output.txt', 'w', encoding='utf-8') as f:
        f.write('Popular Cities Forecast\n')
        f.write(today + '\n')
        f.write('='*23 + '\n')
        table = tabulate(data, headers=['City', 'Temp.', 'Condition'], tablefmt="fancy_grid")
        f.write(table)


def get_forecast_json():
    """
    Save weather data to a JSON file (output.json) with structured format.
    """
    data = get_forecast_data()
    if not isinstance(data, list):
        print(data)
        return

    today = date.today().strftime('%d/%m/%Y')
    cities = [{'city': city, 'temp': temp, 'condition': condition} for city, temp, condition in data]
    data_json = {'title': 'Popular Cities Forecast', 'date': today, 'cities': cities}

    with open('output.json', 'w', encoding='utf-8') as f:
        json.dump(data_json, f, ensure_ascii=False, indent=4)


if __name__ == '__main__':
    get_forecast_txt()
    get_forecast_json()
