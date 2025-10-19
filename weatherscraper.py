import re
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup


def get_forecast_data():
    """Fetch and display weather forecast data from world-weather.info"""

    # Configure Chrome browser options
    options = Options()
    options.add_argument('--headless')
    options.add_argument('--disable-gpu')
    options.add_argument('--no-sandbox')
    options.add_argument('--log-level=3')

    # Disable images and media to speed up loading
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

    # Initialize Chrome WebDriver
    driver = webdriver.Chrome(options=options)

    # Visit website to register domain before adding cookie
    driver.get("https://world-weather.info/")

    # Add cookie to enable Celsius temperature display
    driver.add_cookie({"name": "celsius", "value": "1"})
    driver.refresh()

    # Parse page source with BeautifulSoup
    html = driver.page_source
    soup = BeautifulSoup(html, "html.parser")

    # Locate the main section that contains forecast data
    resorts = soup.find("div", id="resorts")

    # Extract city names using regular expressions
    re_cities = r'">([\w\s]+)</a><span>'
    cities = re.findall(re_cities, str(resorts))

    # Extract temperatures
    re_temps = r'<span>(\+\d+|-\d+)<span'
    temps = [int(temp) for temp in re.findall(re_temps, str(resorts))]

    # Extract weather conditions (tooltip titles)
    conditions_tags = resorts.find_all('span', class_='tooltip')
    conditions = [tag.get('title') for tag in conditions_tags]

    # Combine city, temperature, and condition into one list
    data = list(zip(cities, temps, conditions))

    # Print the final result
    print(data)

    # Close browser
    driver.quit()


get_forecast_data()
