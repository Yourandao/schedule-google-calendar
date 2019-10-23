import pickle
import os

from components.event_object import EventObject
from components.excel_worker import ExcelWorker, EXCEL_HEADER_SCRAP

from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request

class GoogleProcessor:
    def __init__(self, client_name : str):
        self.__scopes = ['https://www.googleapis.com/auth/calendar.readonly','https://www.googleapis.com/auth/calendar']
        self.__creds  = None
        self.service  = None

        if os.path.exists(f'./files\\users\\{client_name}'):
            if os.path.exists(f'./files\\users\\{client_name}\\token.pickle'):
                with open(f'./files\\users\\{client_name}\\token.pickle', 'rb') as token:
                    self.__creds = pickle.load(token)
        else:
            os.mkdir(f'./files\\users\\{client_name}')

        if not self.__creds or not self.__creds.valid:
            if self.__creds and self.__creds.expired and self.__creds.refresh_token:
                self.__creds.refresh(Request())
            else:
                flow = InstalledAppFlow.from_client_secrets_file(f'./files\\creds\\credentials.json', [self.__scopes[1]])
                self.__creds = flow.run_local_server(port=0)

            with open(f'./files\\users\\{client_name}\\token.pickle', 'wb') as token:
                pickle.dump(self.__creds, token)


        self.service = build('calendar', 'v3', credentials = self.__creds)

    def parse_and_push(self):
        all_doubles = 6 * 12
        worker = ExcelWorker('KBiSP-3-kurs-1-sem.xlsx')

        for i in range(EXCEL_HEADER_SCRAP + 54, all_doubles + EXCEL_HEADER_SCRAP, 1):
            row = worker.get_row(i)

            for event in row:
                self.push_to_google_calendar(event)

    def push_to_google_calendar(self, event : EventObject):
        start_time, end_time = event.time.split('-')
        start = event.date.strftime('%Y-%m-%d') + "T" + start_time + ':00'
        end = event.date.strftime('%Y-%m-%d') + "T" + end_time + ':00'
        event_to_push = {
            'summary' : event.subject,
            'location' : event.location,
            'start' : {
                'dateTime' : start,
                'timeZone' : 'Europe/Moscow'
            },
            'end' : {
                'dateTime' : end,
                'timeZone' : 'Europe/Moscow'
            },
            'colorId' : event.color
        }

        self.service.events().insert(calendarId = 'cdv7ihf7p3qro5fto5ve4rp47s@group.calendar.google.com', body=event_to_push).execute()