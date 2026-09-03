import time
import network
from network_time import connect_wifi_forever, sync_time
from display import scroll_message
from date_screen import date_string
from weather import fetch_weather
from messages import get_current_message
from machine import WDT

wdt = WDT(timeout=8000)

print("Booting...")
connect_wifi_forever(wdt=wdt)
wdt.feed()

if not sync_time(wdt=wdt):
    print("NTP failed at boot, will retry in main loop")
wdt.feed()

last_ntp_sync = time.time()

def ensure_wifi():
    wlan = network.WLAN(network.STA_IF)
    if not wlan.isconnected():
        print("Wi-Fi dropped, reconnecting...")
        connect_wifi_forever(wdt=wdt)

def weather_screens():
    try:
        w = fetch_weather()
        return [
            "HI {}F LO {}F UV {}".format(w["high"], w["low"], w["uv"]),
            "RAIN {}%".format(w["precip_chance"]),
            "RISE {} SET {}".format(w["sunrise"], w["sunset"]),
        ]
    except Exception as e:
        print("Weather fetch failed:", e)
        return ["WEATHER UNAVAILABLE"]

cached_weather_screens = weather_screens()
wdt.feed()
cached_message = get_current_message()
wdt.feed()

last_weather_fetch = 0
last_message_fetch = 0

print("Entering main loop")

while True:
    try:
        ensure_wifi()
        wdt.feed()

        if time.time() - last_message_fetch > 30:
            cached_message = get_current_message()
            last_message_fetch = time.time()

        scroll_message(date_string(), wdt=wdt)

        if time.time() - last_weather_fetch > 1800:
            cached_weather_screens = weather_screens()
            last_weather_fetch = time.time()

        for screen in cached_weather_screens:
            scroll_message(screen, wdt=wdt)

        if cached_message:
            scroll_message(cached_message, wdt=wdt)

        if time.time() - last_ntp_sync > 86400:
            sync_time(wdt=wdt)
            last_ntp_sync = time.time()

    except Exception as e:
        print("Loop error:", e)
        time.sleep(5)

    time.sleep(1)
    wdt.feed()