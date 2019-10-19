import urllib.request
import requests
import datetime
import os
import json
import hashlib
import re

FILENAME = 'KBiSP-3-kurs-1-sem.xlsx'

# bold red - не лабы на стромынке
# red - лабы на стромынке
# blue - ЮЗ
# purple - лабы юз

class Updater:
    @staticmethod
    def get_schedule_link(url : str):
        inner_html = requests.get(url).text

        match = re.search(r'<a\sclass=\"xls\"\shref=\"(https://www\.mirea\.ru/upload/medialibrary/[a-zA-Z]{2}[0-9]/KBiSP-3-kurs-1-sem\.xlsx)\"', inner_html)
        if match:
            return match.group(1)
        return None

    @staticmethod
    def update():
        schedule_dir = os.path.join(os.getcwd(), f'files\\data\\{FILENAME}')
        data_dir = os.path.join(os.getcwd(), 'files\\data\\data.json')
        hasher = hashlib.sha1()

        if not os.path.exists(schedule_dir) and not os.path.exists(data_dir):
            with open(data_dir, 'w') as data:
                schedule_href = Updater.get_schedule_link('https://www.mirea.ru/education/schedule-main/schedule/')
                urllib.request.urlretrieve(schedule_href, schedule_dir)

                with open(schedule_dir, 'r', encoding='utf-8', errors='ignore') as schedule_sheet:
                    hasher.update(schedule_sheet.read().encode('utf-8'))
                    data.write(json.dumps({'name': FILENAME, 'checksum': \
                                hasher.hexdigest(), 'date': datetime.datetime.now().strftime("%Y-%m-%d;%H:%M")}))
        else:
            with open(data_dir, 'r+') as data:
                with open(schedule_dir, 'r', encoding='utf-8', errors='ignore') as schedule_sheet:
                    hasher.update(schedule_sheet.read().encode('utf-8'))

                    if int(json.loads(data.read())['checksum']) != hasher.hexdigest():
                        schedule_href = f'https://www.mirea.ru//upload//medialibrary//89c//{FILENAME}'
                        urllib.request.urlretrieve(schedule_href, schedule_dir)

                        data.write({'name': FILENAME, 'checksum': hasher.hexdigest(), 'date': datetime.datetime.now()})

Updater.update()