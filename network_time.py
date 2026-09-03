import network
import time
import ntptime
from secrets import WIFI_SSID, WIFI_PASSWORD

def connect_wifi(timeout=15, wdt=None):
    wlan = network.WLAN(network.STA_IF)
    wlan.active(False)
    time.sleep(0.5)
    wlan.active(True)
    wlan.config(pm=network.WLAN.PM_NONE)
    wlan.connect(WIFI_SSID, WIFI_PASSWORD)

    start = time.time()
    while not wlan.isconnected():
        if time.time() - start > timeout:
            print("Wi-Fi status code:", wlan.status())
            raise RuntimeError("Wi-Fi connection timed out")
        time.sleep(0.5)
        if wdt:
            wdt.feed()

    time.sleep(1)
    print("Connected:", wlan.ifconfig())
    return wlan

def connect_wifi_forever(timeout=15, wdt=None, max_backoff=60):
    """Keeps retrying indefinitely, backing off, never crashes the caller."""
    delay = 2
    while True:
        try:
            return connect_wifi(timeout=timeout, wdt=wdt)
        except Exception as e:
            print("Wi-Fi connect failed:", e, "- retrying in", delay, "s")
            waited = 0
            while waited < delay:
                time.sleep(1)
                waited += 1
                if wdt:
                    wdt.feed()
            delay = min(delay * 2, max_backoff)

def sync_time(retries=5, wdt=None):
    for attempt in range(retries):
        try:
            ntptime.settime()
            print("Time synced (UTC)")
            return True
        except Exception as e:
            print("NTP attempt {} failed: {}".format(attempt + 1, e))
            time.sleep(3)
            if wdt:
                wdt.feed()
    print("NTP sync failed after all retries")
    return False

def _nth_sunday(year, month, n):
    t = time.mktime((year, month, 1, 0, 0, 0, 0, 0))
    wday = time.localtime(t)[6]
    days_to_sunday = (6 - wday) % 7
    first_sunday = 1 + days_to_sunday
    return first_sunday + (n - 1) * 7

def is_dst(year, month, day, hour):
    dst_start_day = _nth_sunday(year, 3, 2)
    dst_end_day = _nth_sunday(year, 11, 1)

    if month < 3 or month > 11:
        return False
    if 3 < month < 11:
        return True
    if month == 3:
        return (day > dst_start_day) or (day == dst_start_day and hour >= 2)
    if month == 11:
        return (day < dst_end_day) or (day == dst_end_day and hour < 2)

def local_time():
    utc = time.localtime()
    year, month, day, hour = utc[0], utc[1], utc[2], utc[3]

    offset = -4 if is_dst(year, month, day, hour) else -5
    adjusted = time.mktime(utc) + offset * 3600
    return time.localtime(adjusted)