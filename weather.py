import requests
import database


def get_weather(city: str) -> dict | None:
    """
    Query OpenWeatherMap for current weather in the given city.
    Requires a valid API key stored in the database.
    """
    api_key = database.load_api_key()
    if not api_key:
        raise ValueError("No API key found in database. Please set it first.")

    url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}&units=metric"

    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        data = response.json()

        # Extract relevant info
        weather_info = {
            "city": data.get("name"),
            "temperature": data["main"]["temp"],
            "description": data["weather"][0]["description"],
            "icon": data["weather"][0]["icon"],
            "humidity": data["main"]["humidity"],
            "wind_speed": data["wind"]["speed"],
        }
        return weather_info

    except requests.exceptions.RequestException as e:
        print(f"Error querying OpenWeatherMap: {e}")
        return None
