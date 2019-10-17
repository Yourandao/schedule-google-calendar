import pickle
import os.path

from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request

class GoogleProcessor:
    def __init__(self, creds_path : str, client_name : str):
        self.__scopes = ['https://www.googleapis.com/auth/calendar.readonly','https://www.googleapis.com/auth/calendar']
        self.__creds  = None
        self.service  = None

        if os.path.exists(f'files\\users\\{client_name}'):
            if os.path.exists(f'files\\users\\{client_name}\\token.pickle'):
                with open(f'files\\users\\{client_name}\\token.pickle', 'rb') as token:
                    self.__creds = pickle.load(token)
        else:
            os.mkdir(f'files\\users\\{client_name}')

        if not self.__creds or not self.__creds.valid:
            if self.__creds and self.__creds.expired and self.__creds.refresh_token:
                self.__creds.refresh(Request())
            else:
                flow = InstalledAppFlow.from_client_secrets_file(os.path.join(os.getcwd(), f'files\\creds\\credentials.json'), [self.__scopes[1]])
                self.__creds = flow.run_local_server(port=0)

            with open(f'files\\users\\{client_name}\\token.pickle', 'wb') as token:
                pickle.dump(self.__creds, token)


        self.service = build('calendar', 'v3', credentials = self.__creds)

    def push_to_google_calendar(self, summary : str, location : str, start : str, end : str):
        event_to_push = {
            'summary' : summary,
            'location' : location,
            'start' : {
                'dateTime' : start,
                'timeZone' : 'Europe/Moscow'
            },
            'end' : {
                'dateTime' : end,
                'timeZone' : 'Europe/Moscow'
            }
        }

        self.service.events().insert(calendarId = 'primary', body=event_to_push).execute()