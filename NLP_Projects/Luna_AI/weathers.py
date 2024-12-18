import requests

API_KEY = ""# Use here yoour key

def get_weather(city):
    base_url = "http://api.openweathermap.org/data/2.5/weather?"
    complete_url = base_url + "appid=" + API + "&q=" + city
    response = requests.get(complete_url)
    data = response.json()
    if data["cod"] != "404":
        main = data["main"]
        weather_desc = data["weather"][0]["description"]
        temp = main["temp"] - 273.15  # Convert from Kelvin to Celsius
        return f"The temperature in {city} is {temp:.2f}°C with {weather_desc}."
    else:
        return "City not found."
    
