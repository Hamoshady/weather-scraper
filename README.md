# 🌦️ Weather Forecast Scraper

## 📘 Overview
This Python script scrapes **weather forecast data** (city name, temperature, and weather condition)  
from [World Weather Info](https://world-weather.info/).

It uses:
- **Selenium** → to load the webpage and handle cookies dynamically.  
- **BeautifulSoup** → to parse HTML and extract the relevant information.  
- **Regular Expressions** → to identify city names and temperatures in the HTML.  
- **Tabulate** → to create a nicely formatted table in the TXT file.  
- **JSON module** → to save structured data in a readable JSON file.

---

## ⚙️ Features
✅ Automatically enables **Celsius** mode using cookies  
✅ Extracts **city names**, **temperatures**, and **weather conditions**  
✅ Runs **headless** (no browser window) for speed and automation  
✅ Optimized to **disable images and plugins** to load faster  
✅ **Type hints** added for better code clarity and maintainability  
✅ Saves output in **TXT** (`output.txt`) and **JSON** (`output.json`) formats  
✅ **JSON output is indented** for readability  
✅ **Error handling** added to prevent crashes if data is missing  

---

## 🧩 Requirements
Make sure you have the following installed:

```bash
pip install selenium beautifulsoup4 tabulate
