# google-calendar-script

# Delete all events for today in a google calendar by using Google Asistant and Google Cloud Functions.

# 1. Google Cloud Setup
### a. Create google cloud account
### b. Enable billing
### c. Create google project
### d. Enable Calendar API
### e. Oauth Consent
### f. Add yourself as test account
### g. Create oauth credentials and save under calendar_credentials.json

# 2. Generate Google Calendar access token
### a. Add the calendar_credentials.json file in the project
### b. Change to your CALENDAR_ID in code. You can find it by going to your calendar settings, should be somewhere on the bottom
### c. Run generate_calendar_token script to generate the token file

# 3. Google Cloud Function Setup
### a. Go to cloud functions and create one. 
### b. Add environment variable CALENDAR ID: Runtime -> Runtime environmental variables -> name: CALENDAR_ID, Value: your calendar id value
### c. Add secrets https://cloud.google.com/functions/docs/configuring/secrets
### d. Reference a secret under Secury and Image repo -> Exposed as env variable, name -> CALENDAR_ACCESS_TOKEN
### e. Copy the requirements.txt file to the cloud function 
### f. Copy the code from delete_events.py to the main.py in google cloud and make sure you add entry point "main" as this the first function to be called

# 4. Google Actions
### a. Create project action linking it to the previously created google project
### b. Enter your app's display name and voice. This is the name of how you will trigger the app from google assistant. If your app name is Stan, then you will ask google "Hey Google, Ask Stan to clean my calendar" 
### c. Create custom global intent CleanUpCalendar 
### d. Add training phrases to the intent - "clear my calendar", "delete events for today", "clean calendar for today", etc
### e. Edit global handling -> enable webhook and send prompts on the right. Add delete_calendar_events event handler and add your own speech response, i.e "Okay I am cleaning up your calendar for today.
### f. Go to webhook and select HTTPS endpoint as fulfillment. 
### g. Enter your function URL 