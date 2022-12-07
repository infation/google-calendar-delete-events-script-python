from google_auth_oauthlib.flow import InstalledAppFlow

# If modifying these scopes, delete the file token.json.
SCOPES = ['https://www.googleapis.com/auth/calendar']

def main():
    """Generates a new token/refresh token under calendar_access_token.json for Google Calendar."""

    creds = None
    # The file token.json stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.

    # If there are no (valid) credentials available, let the user log in.
    flow = InstalledAppFlow.from_client_secrets_file('calendar_credentials.json', SCOPES)
    creds = flow.run_local_server(port=0)

    # Save the credentials
    with open('calendar_access_token.json', 'w') as token:
        token.write(creds.to_json())


if __name__ == '__main__':
    main()