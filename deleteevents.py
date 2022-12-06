from __future__ import print_function

import datetime
import os.path
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

# If modifying these scopes, delete the file token.json.
SCOPES = ['https://www.googleapis.com/auth/calendar.readonly']


calendarId = os.environ["CALENDAR_ID"]
calendarCredentialsPath = os.environ["CALENDAR_CREDENTIALS_PATH"]

def main():
    """Shows basic usage of the Google Calendar API.
    Prints the start and name of the next 10 events on the user's calendar.
    """


    creds = None
    # The file token.json stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
    if os.path.exists(calendarCredentialsPath + '/token.json'):
        creds = Credentials.from_authorized_user_file(calendarCredentialsPath + '/token.json', SCOPES)
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                calendarCredentialsPath + '/calendar_credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)
        # Save the credentials for the next run
        with open(calendarCredentialsPath + '/token.json', 'w') as token:
            token.write(creds.to_json())

    try:
        service = build('calendar', 'v3', credentials=creds)

        # Call the Calendar API
        now = datetime.datetime.utcnow()
        start = now.replace(hour=0, minute=0, second=0, microsecond=1).isoformat() + 'Z'  # 'Z' indicates UTC time
        end = now.replace(hour=23, minute=59, second=59, microsecond=999999).isoformat() + 'Z'
        print('Getting events between ' + start + ' and ' + end)
        events_result = service.events().list(calendarId=calendarId, timeMin=start, timeMax=end, singleEvents=True, orderBy='startTime').execute()
        events = events_result.get('items', [])

        if not events:
            print('No upcoming events found.')
            return

        # Prints the start and name of the next 10 events
        for event in events:
            start = event['start'].get('dateTime', event['start'].get('date'))
            print(start, event['summary'])

    except HttpError as error:
        print('An error occurred: %s' % error)


if __name__ == '__main__':
    main()