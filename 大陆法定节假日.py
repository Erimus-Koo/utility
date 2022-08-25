#!/usr/bin/env python3
# -*- coding: utf-8 -*-
__author__ = 'Erimus'
# 读取 iCalendar 分享的日历，导出具体的放假日及补假工作日。

import requests
import re
from datetime import datetime, timedelta
from pprint import pp

# ═══════════════════════════════════════════════


class China_Statutory_Holidays():
    def __init__(self):
        r = requests.get('https://p42-caldav.icloud.com/published/2/Mjk1MjUyNzU2Mjk1MjUyN3InbiAUgtR-77GMA1aDk_4tLextGI1NIjkDeSYbJgMnkBfggxSBN5Q-OKqIOcv0xDkmRJKU5s5tHyuOgqabBv0')
        # print(r.text)

        self.holiday_dict = {'workday': {}, 'holiday': {}}
        for event in re.findall(r'(?s)(?<=BEGIN:VEVENT).*?(?=END:VEVENT)', r.text):
            start = re.search(r'(?<=DTSTART;VALUE=DATE:)\d{8}', event).group()
            end = re.search(r'(?<=DTEND;VALUE=DATE:)\d{8}', event).group()
            info = re.search(r'(?<=SUMMARY:).*?\n', event).group().strip()
            # print(f'{start} --> {end = } | {info}')

            start_dt = datetime.strptime(start, '%Y%m%d')
            end_dt = datetime.strptime(end, '%Y%m%d')
            while start_dt <= end_dt:
                self.holiday_dict['workday' if '上班' in info else 'holiday'].update(
                    {datetime.strftime(start_dt, '%Y-%m-%d'): info})
                start_dt += timedelta(1)

        # pp(self.holiday_dict, sort_dicts=True)

    def show(self):
        pp(self.holiday_dict, sort_dicts=True)

    def next_workday(self):
        this_day = datetime.now()
        while 1:
            this_day += timedelta(1)
            fmt_this_day = datetime.strftime(this_day, '%Y-%m-%d')
            if fmt_this_day in self.holiday_dict['workday']:
                return this_day
            elif (fmt_this_day in self.holiday_dict['holiday']
                  or this_day.weekday() in [5, 6]):
                continue
            else:
                return this_day

    def is_today_workday(self):
        this_day = datetime.now()
        fmt_this_day = datetime.strftime(this_day, '%Y-%m-%d')
        if fmt_this_day in self.holiday_dict['workday']:
            return True
        elif (fmt_this_day in self.holiday_dict['holiday']
              or this_day.weekday() in [5, 6]):
            return False
        else:
            return True


# ═══════════════════════════════════════════════
if __name__ == '__main__':

    holiday = China_Statutory_Holidays()
    print(f'{holiday.is_today_workday() = }')
    print(f'{holiday.next_workday() = }')
