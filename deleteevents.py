from __future__ import print_function

import datetime
import pytz
import os.path
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

# If modifying these scopes, delete the file token.json.
SCOPES = ['https://www.googleapis.com/auth/calendar']


calendarId = os.environ["CALENDAR_ID"]
calendarCredentialsPath = os.environ["CALENDAR_CREDENTIALS_PATH"]

def main():
    """Deletes all events on scheduled for today on Google Calendar."""

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
        #Build the service and retrieve the Calendar object
        service = build('calendar', 'v3', credentials=creds)
        calendar = service.calendars().get(calendarId=calendarId).execute()

        #Get the calendar timezone and the current start / end of the day for that specific timezone
        currentTimeInTimezone = datetime.datetime.now(pytz.timezone(calendar['timeZone']))
        dayStart = currentTimeInTimezone.replace(hour=0, minute=0, second=0, microsecond=1).isoformat()
        dayEnd = currentTimeInTimezone.replace(hour=23, minute=59, second=59, microsecond=999999).isoformat()

        print('Getting events between ' + dayStart + ' and ' + dayEnd)

        # Get the events
        events_result = service.events().list(calendarId=calendarId, timeMin=dayStart, timeMax=dayEnd, singleEvents=True, orderBy='startTime').execute()
        events = events_result.get('items', [])

        if not events:
            print('No upcoming events found.')
            return

        #Call Calendar API and remove all events for today
        for event in events:
            service.events().delete(calendarId=calendarId, eventId=event['id']).execute()

    except HttpError as error:
        print('An error occurred: %s' % error)


if __name__ == '__main__':
    main()