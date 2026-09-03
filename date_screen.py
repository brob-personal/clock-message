from network_time import local_time

MONTHS = ["JAN", "FEB", "MAR", "APR", "MAY", "JUN",
          "JUL", "AUG", "SEP", "OCT", "NOV", "DEC"]
DAYS = ["MON", "TUE", "WED", "THU", "FRI", "SAT", "SUN"]

def date_string():
    t = local_time()
    year, month, day, hour, minute, second, weekday, yearday = t
    return "{}  {} {}".format(DAYS[weekday], MONTHS[month - 1], day)

if __name__ == "__main__":
    print(date_string())