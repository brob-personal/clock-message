import urequests
from secrets import AIO_USERNAME, AIO_KEY, AIO_FEED

URL = "https://io.adafruit.com/api/v2/{}/feeds/{}/data/last?x-aio-key={}".format(
    AIO_USERNAME, AIO_FEED, AIO_KEY
)

def get_current_message():
    response = None
    try:
        response = urequests.get(URL)
        data = response.json()
    except Exception as e:
        print("Message check failed:", e)
        return None
    finally:
        if response:
            response.close()

    if "value" not in data:
        return None
    return data["value"]

if __name__ == "__main__":
    from network_time import connect_wifi
    connect_wifi()
    print(get_current_message())