import network
import time
import ntptime
from secrets import WIFI_SSID, WIFI_PASSWORD

def connect_wifi(timeout=15):
    wlan = network.WLAN(network.STA_IF)
    wlan.active(True)
    wlan.connect(WIFI_SSID, WIFI_PASSWORD)

    start = time.time()
    while not wlan.isconnected():
        if time.time() - start > timeout:
            raise RuntimeError("Wi-Fi connection timed out")
        time.sleep(0.5)

    print("Connected:", wlan.ifconfig())
    return wlan

def sync_time():
    try:
        ntptime.settime()
        print("Time synced (UTC)")
    except Exception as e:
        print("NTP sync failed:", e)

def _nth_sunday(year, month, n):
    # Find the nth Sunday of a given month/year
    t = time.mktime((year, month, 1, 0, 0, 0, 0, 0))
    wday = time.localtime(t)[6]  # 0 = Monday in MicroPython's time tuple
    days_to_sunday = (6 - wday) % 7
    first_sunday = 1 + days_to_sunday
    return first_sunday + (n - 1) * 7

def is_dst(year, month, day, hour):
    # US DST: starts 2nd Sunday in March, ends 1st Sunday in November
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
    utc = time.localtime()  # RTC is set to UTC by ntptime
    year, month, day, hour = utc[0], utc[1], utc[2], utc[3]

    offset = -4 if is_dst(year, month, day, hour) else -5
    adjusted = time.mktime(utc) + offset * 3600
    return time.localtime(adjusted)

if __name__ == "__main__":
    connect_wifi()
    sync_time()
    print("UTC:", time.localtime())
    print("Local (EST/EDT):", local_time())