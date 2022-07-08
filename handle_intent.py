from selenium.webdriver.chrome.service import Service
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from geopy.geocoders import Nominatim
from newsapi import NewsApiClient
from datetime import datetime
import osascript
import wikipedia
import requests
import numpy as np
import cv2
import pyautogui
import os

# User Modules
from aardvark_speaks import aardvark_says
import capture_voice

# Constants
OPEN_WEATHER_KEY = os.getenv('OPEN_WEATHER_KEY')
OPEN_WEATHER_KEY = '54263f49323163b8be8c1084109d69cc'

YOUTUBE_SEARCH_URL = 'https://www.youtube.com/results?search_query='

# Selenium Setup
service = Service(executable_path="/Users/derekbeistad/Development/chromedriver")


def open_in_chrome(url):
    driver = webdriver.Chrome(service=service)
    driver.get(url)
    driver.minimize_window()


def translate_weather_id(category_id):
    """
    translated the weather category id from the API into a string
    :param id:
    :return category:
    """
    if category_id == 800:
        category = 'clear'
    elif category_id == 801 or category_id == 802:
        category = 'partly cloudy'
    elif category_id == 803 or category_id == 804:
        category = 'cloudy'
    elif 600 <= category_id <= 622:
        category = 'snowy'
    elif category_id == 500 or category_id == 501:
        category = 'lightly raining'
    elif category_id == 511:
        category = 'freezing rain'
    elif 520 <= category_id <= 599:
        category = 'raining'
    elif 300 <= category_id <= 399:
        category = 'drizzling'
    elif 200 <= category_id <= 299:
        category = 'thunderstorming'
    else:
        category = 'unknown'
    return category


def get_current_weather(location_text):
    """
    Fetches the current weather conditions for a specific location from Open Weather.
    Gathers the Longitude and Latitude from location text then uses requests to get weather data.
    :param location_text:
    :return: a dictionary {'weather_category': a string describing overall conditions,
        'weather_temperature': an int in fahrenheit,
        'weather_humidity': percent humidity as a string,
        'weather_wind_speed': an int in mph,
        'weather_city': city name as a string}

    """
    geolocator = Nominatim(user_agent="Aardvark")
    try:
        location = geolocator.geocode(location_text)
        lat, lon = location.latitude, location.longitude
    except:
        print("Failed to get location, Please try again.")
    response = requests.get(
        f'https://api.openweathermap.org/data/2.5/weather?lat={lat}&lon={lon}&appid={OPEN_WEATHER_KEY}').json()
    category_id = response['weather'][0]['id']
    category = translate_weather_id(category_id)
    weather_category = category
    weather_temperature = (response['main']['temp'] - 273.15) * 9 / 5 + 32
    weather_humidity = str(response['main']['humidity']) + '%'
    weather_wind_speed = response['wind']['speed'] * 2.237
    weather_city = response['name']
    current_weather = {
        'weather_category': weather_category,
        'weather_temperature': int(round(weather_temperature)),
        'weather_humidity': weather_humidity,
        'weather_wind_speed': int(round(weather_wind_speed)),
        'weather_city': weather_city
    }
    return current_weather


def get_tomorrow_weather(location_text):
    """
    Fetches the weather for tomorrow for a specific location from Open Weather.
    Gathers the Longitude and Latitude from location text then uses requests to get weather data.
    :param location_text:
    :return: a dictionary {'weather_category': a string describing overall conditions,
        'weather_temperature': an int in fahrenheit,
        'weather_humidity': percent humidity as a string,
        'weather_wind_speed': an int in mph,
        'weather_city': city name as a string}

    """
    geolocator = Nominatim(user_agent="Aardvark")
    try:
        location = geolocator.geocode(location_text)
        lat, lon = location.latitude, location.longitude
    except:
        print("Failed to get location, Please try again.")
    response = requests.get(
        f'https://api.openweathermap.org/data/2.5/forecast?lat={lat}&lon={lon}&appid={OPEN_WEATHER_KEY}').json()
    weather = response['list'][4]
    category_id = weather['weather'][0]['id']
    category = translate_weather_id(category_id)
    weather_category = category
    weather_temperature = (weather['main']['temp'] - 273.15) * (9 / 5) + 32
    weather_humidity = str(weather['main']['humidity']) + '%'
    weather_wind_speed = weather['wind']['speed'] * 2.237
    weather_city = response['city']['name']
    tomorrow_weather = {
        'weather_category': weather_category,
        'weather_temperature': int(round(weather_temperature)),
        'weather_humidity': weather_humidity,
        'weather_wind_speed': int(round(weather_wind_speed)),
        'weather_city': weather_city
    }
    return tomorrow_weather


def print_weather_dict(weather_dict):
    """
    Prints the weather data gathers from the get_current_weather
    function in the console.
    :param weather_dict:
    :return:
    """
    print('category: ', weather_dict["weather_category"])
    print('temperature: ', weather_dict["weather_temperature"])
    print('humidity: ', weather_dict["weather_humidity"])
    print('wind speed: ', weather_dict["weather_wind_speed"])
    print('city: ', weather_dict["weather_city"])


def search_google(key_words):
    """
    Uses Selenium to open a Google search for key word inputs in Google Chrome.
    :param key_words:
    :return:
    """
    url = f'https://www.google.com/search?q={key_words}'
    open_in_chrome(url)
    print('Google has opened in your browser.')


def get_wikipedia_summary(search_prompt):
    """
    Uses the Wikipedia module to get the first 2 sentences of a queried topic.
    :param search_prompt:
    :return: string with 2 sentence summary
    """
    try:
        search_summary = wikipedia.summary(search_prompt, sentences=2)
    except wikipedia.exceptions.DisambiguationError as e:
        print(e.options)
    except wikipedia.exceptions.PageError:
        return f"I did not find anything about {search_prompt}."
    return search_summary


def play_song_on_youtube(video_title):
    """
    Uses Selenium to open a search on YouTube in Google Chrome then begins
    to play the first video in the listing.
    :param video_title:
    :return:
    """
    driver = webdriver.Chrome(service=service)
    wait = WebDriverWait(driver, 3)
    visible = EC.visibility_of_element_located
    clickable = EC.element_to_be_clickable

    driver.get(f'{YOUTUBE_SEARCH_URL}{video_title}')
    wait.until(visible((By.ID, "video-title")))
    driver.find_element(By.ID, "metadata-line").click()
    try:
        wait.until(clickable((By.XPATH, "//*[@id='skip-button:6']/span/button"))).click()
    except:
        print("no skip button")
    print('Song has opened in your browser.')


def get_directions(from_location, to_loocation):
    """
    Uses Selenium to open a window in Google Chrome with directions
    from a input location to a second input location via Google Maps.
    :param from_location:
    :param to_loocation:
    :return:
    """
    url = f'https://www.google.com/maps/dir/{from_location}/{to_loocation}'
    open_in_chrome(url)
    print('Directions have opened in your browser.')


def open_news():
    """
    Opens Google News in Google Chrome using Selenium
    :return:
    """
    url = 'https://news.google.com/topstories'
    open_in_chrome(url)
    aardvark_says('News has been opened in your browser.')


def take_screenshot():
    """
    Uses os.path to get a path to save image on Desktop.
    Captures a screenshot using pyautogui then saves the image
    to the Desktop with the image name of 'aardvark_screenshot_{num}.png'
    :return:
    """
    num = 1
    image_name = f"aardvark_screenshot_{num}.png"
    desktop = os.path.normpath(os.path.expanduser("~/Desktop"))
    path = os.path.join(desktop, image_name)
    image = pyautogui.screenshot()
    image = cv2.cvtColor(np.array(image), cv2.COLOR_RGB2BGR)
    while True:
        if os.path.isfile(path):
            num += 1
            image_name = f"aardvark_screenshot_{num}.png"
            desktop = os.path.normpath(os.path.expanduser("~/Desktop"))
            path = os.path.join(desktop, image_name)
        else:
            cv2.imwrite(path, image)
            print('Screenshot saved to Desktop')
            break


def tell_joke():
    """
    Uses the requests module to get a random dad joke from the icanhazdadjoke api
    :return: joke as a string
    """
    headers = {"User-Agent": "Practice Desktop App for portfolio.; email: derek18b@gmail.com",
               "Accept": "text/plain"}
    response = requests.get('https://icanhazdadjoke.com/', headers=headers)
    if 200 <= response.status_code <= 299:
        return response.text
    else:
        return "error finding the best joke. try this instead: " \
               "Why don't ants get sick?... They have anty-bodies."


def get_quote():
    """
    Uses the requests module to get a random philisophical quote from the stoic quotes api
    :return: quote as a string
    """
    response = requests.get('https://stoicquotesapi.com/v1/api/quotes/random')
    response_json = response.json()
    quote = response_json['body'] + ' ... - ' + response_json['author']

    if 200 <= response.status_code <= 299:
        return quote
    else:
        return "error finding a quote. try this instead: " \
               '“Wonder is the beginning of wisdom.” ... ― Socrates .'


def get_time():
    """
    uses the datetime library to return the current time in the HH:MM AM/PM format
    :return: HH:MM AM/PM
    """
    return datetime.now().strftime("%I:%M %p")


def get_date():
    """
    uses the datetime library to return the current date in the 'Today is {day_name}, {month} {day} {year}' format
    :return: today's date as a string
    """
    date = datetime.today()
    day_name, day = date.strftime("%A"), date.strftime("%d")
    month, year = date.strftime("%B"), date.strftime("%Y")
    if day == '01':
        today = f"Today is {day_name}, {month} {day}st {year}"
    if day == '02':
        today = f"Today is {day_name}, {month} {day}nd {year}"
    if day == '03':
        today = f"Today is {day_name}, {month} {day}rd {year}"
    else:
        today = f"Today is {day_name}, {month} {day}th {year}"
    return today


def adjust_computer_volume(command):
    """
    Uses osascript to adjust the computer volume via command
    :param command:
    :return: string dictating if volume was turned up or down
    """
    code, volume, err = osascript.run("output volume of (get volume settings)")
    volume = int(volume)
    if 'up' in command:
        volume += 10
        volume_adjustment = "Volume turned up."
    elif 'down' in command:
        volume -= 10
        volume_adjustment = "Volume turned down."
    osascript.osascript(f"set volume output volume {volume}")
    return volume_adjustment
