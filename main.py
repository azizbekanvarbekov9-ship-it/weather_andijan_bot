"""Usbu kod har daqiqaning 5-soniyasida Toshkent shahrining ob-havo ma'lumotlarini olish uchun mo'ljallangan."""
import time
import datetime as dt


from scheduler import Scheduler


from functions import get_andijon_weather


schedule = Scheduler()


schedule.daily(dt.time(hour=7, minute=0), get_andijon_weather)
print(schedule)


while True:
    schedule.exec_jobs()
    time.sleep(1)
