import urequests
from secrets import LATITUDE, LONGITUDE

URL = (
    "https://api.open-meteo.com/v1/forecast"
    "?latitude={}&longitude={}"
    "&daily=temperature_2m_max,temperature_2m_min,uv_index_max,"
    "precipitation_probability_max,sunrise,sunset"
    "&temperature_unit=fahrenheit"
    "&timezone=America%2FNew_York"
).format(LATITUDE, LONGITUDE)

def fetch_weather():
    response = None
    try:
        response = urequests.get(URL)
        data = response.json()
    finally:
        if response:
            response.close()

    daily = data["daily"]
    return {
        "high": round(daily["temperature_2m_max"][0]),
        "low": round(daily["temperature_2m_min"][0]),
        "uv": round(daily["uv_index_max"][0]),
        "precip_chance": daily["precipitation_probability_max"][0],
        "sunrise": daily["sunrise"][0][-5:],
        "sunset": daily["sunset"][0][-5:],
    }

if __name__ == "__main__":
    from network_time import connect_wifi
    connect_wifi()
    print(fetch_weather())