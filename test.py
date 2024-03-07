import os

from langchain_community.utilities import OpenWeatherMapAPIWrapper

os.environ["OPENWEATHERMAP_API_KEY"] =  "a15039154ac226a73909c312586ea4c8"

weather = OpenWeatherMapAPIWrapper()

weather_data = weather.run("London,GB")
print(weather_data)