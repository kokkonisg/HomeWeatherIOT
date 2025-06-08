import requests
import time
import json
from win10toast import ToastNotifier

# TODO:
#   When to request the next temperature should be based 
#   on the difference between the last in and out temp
#   so the ESP doesnt waste power
#   (ex. if the diff is 5 C you shouldnt open the windows in the next hours)
#   (so why check the temp every 5 minutes)

# -----------------------------------------------------------------------------------------------------------
# UNTIL I get the ESP8266 working, I will use this to simulate the temperature input.
# Server will also be running on ESP8266
# TODO:
#   Using an ESP8266 get temp inside the house using a DS18B20 sensor
tempIn = float(input("Enter temperature in Celsius: "))
try:
    response = requests.post(    
        url = 'http://localhost:8080/temperature',
        json = {'timestamp': time.strftime('%H:%M:%S', time.localtime()),'temperature_c': str(tempIn)}
    )
except requests.exceptions.RequestException as e:
    print(f"Error fetching weather data: {e}")
# -----------------------------------------------------------------------------------------------------------

# Get coord and API key from info.txt
with open('info.txt', 'r') as f:
    info = f.read().strip().split(',')

# Get current weather data from OpenWeatherMap API
try:
    httpOWMReq = requests.get(
        url=f'https://api.openweathermap.org/data/2.5/weather?lat={info[0]}&lon={info[1]}&appid={info[2]}&units=metric',
    )
except requests.exceptions.RequestException as e:
    print(f"Error fetching weather data: {e}")

curWeatherData = httpOWMReq.json()
tempOut = curWeatherData['main']['temp']

# Get forecast data from OpenWeatherMap API
try:
    httpOWMForecastReq = requests.get(
        url=f'https://api.openweathermap.org/data/2.5/forecast?lat={info[0]}&lon={info[1]}&appid={info[2]}&units=metric&cnt=2',
    )
    nextWeatherData = httpOWMForecastReq.json()['list'][1]
except requests.exceptions.RequestException as e:
    print(f"Error fetching weather data: {e}")
    

# Get temperature data from the local server
try:
    httpHomeReq = requests.get(
        url = 'http://localhost:8080/temperature',
    )
    homeData = httpHomeReq.json()
    # tempIn = homeData['temperature_c']
except requests.exceptions.RequestException as e:
    print(f"Error fetching weather data: {e}")

# Check weather conditions in case of rain
willRain = nextWeatherData['weather'][0]['main'] in ['Rain', 'Drizzle', 'Thunderstorm']
# print(f'Temp right now is {tempOut} C outside.') # Just for testing


# Create a notification 
toaster = ToastNotifier()

# If outside temp is lower notify to open windows
if tempIn > tempOut:
    toaster.show_toast(
        "Open your Windows!!!",
        f'Temp right now is {tempOut} C outside.\nInside temp is {tempIn} C',
        duration = 5,
        icon_path = "./favicon.ico",
        threaded=False
    )

# If forecast sais rain, notify to get the clothes in
if willRain:
    toaster.show_toast(
        "Get your Boogada!!!",
        f'Its about to get {nextWeatherData['weather'][0]['main']}y outside.',
        duration = 5,
        icon_path = "./favicon.ico",
        threaded=False
    )

