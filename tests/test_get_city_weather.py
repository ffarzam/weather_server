from HW12.weather_server import get_city_weather


def test_get_city_weather():
    weather_info = get_city_weather("San Francisco")
    assert isinstance(weather_info, dict)
    assert 'temperature' in weather_info["weather_info"]
    assert 'feels_like' in weather_info["weather_info"]
    assert 'last_updated' in weather_info["weather_info"]


def test_get_invalid_city_weather():

    weather_info = get_city_weather("invalid")
    assert isinstance(weather_info, dict)
    assert weather_info["weather_info"]['cod'] == "404"


